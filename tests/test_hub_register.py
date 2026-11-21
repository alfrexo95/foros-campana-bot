import json
import os
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "hub_register.sh"
FAKE_CURL = r'''#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
url = args[-1]
payload = ""
auth_ok = False
for i, arg in enumerate(args):
    if arg == "-d" and i + 1 < len(args): payload = args[i + 1]
    if arg == "--config" and i + 1 < len(args):
        cfg = open(args[i + 1], encoding="utf-8").read()
        auth_ok = "Authorization: Bearer " in cfg and len(cfg.strip()) > 30
status = "503" if os.getenv("FAKE_CURL_REGISTER_FAIL") and url.endswith("/register") else ("201" if url.endswith("/register") else "200")
record = {"url": url, "payload": payload, "auth_ok": auth_ok, "status": status}
with open(os.environ["CURL_LOG"], "a", encoding="utf-8") as f: f.write(json.dumps(record) + "\n")
print(status, end="")
'''

class HubRegisterTests(unittest.TestCase):
    def run_script(self, token=None, fail_register=False):
        with tempfile.TemporaryDirectory() as td:
            tmp = pathlib.Path(td)
            curl = tmp / "curl"
            curl.write_text(FAKE_CURL, encoding="utf-8")
            curl.chmod(0o755)
            log = tmp / "curl.jsonl"
            env = os.environ.copy()
            env["PATH"] = str(tmp) + os.pathsep + env.get("PATH", "")
            env["CURL_LOG"] = str(log)
            env["INFRA_HUB_URL"] = "https://hub.example.test/"
            if token is None: env.pop("INFRA_HUB_TOKEN", None)
            else: env["INFRA_HUB_TOKEN"] = token
            if fail_register: env["FAKE_CURL_REGISTER_FAIL"] = "1"
            else: env.pop("FAKE_CURL_REGISTER_FAIL", None)
            proc = subprocess.run(["bash", str(SCRIPT)], env=env, text=True, capture_output=True, timeout=10)
            records = [json.loads(x) for x in log.read_text(encoding="utf-8").splitlines()] if log.exists() else []
            return proc, records

    def test_missing_secret_skips_without_network(self):
        proc, records = self.run_script()
        self.assertEqual(proc.returncode, 0)
        self.assertIn("skipped", proc.stdout)
        self.assertEqual(records, [])

    def test_registration_then_heartbeat_only(self):
        proc, records = self.run_script(token="test-token-not-real")
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(len(records), 2)
        self.assertTrue(all(x["auth_ok"] for x in records))
        self.assertTrue(records[0]["url"].endswith("/infra/agents/register"))
        payload = json.loads(records[0]["payload"])
        self.assertEqual(payload["agent_id"], "foros-campana-bot")
        self.assertEqual(payload["platform"], "github-actions")
        self.assertEqual(payload["capabilities"], ["forum.publish.botchan", "forum.publish.anystation"])
        self.assertTrue(records[1]["url"].endswith("/infra/agents/foros-campana-bot/heartbeat"))
        self.assertEqual(json.loads(records[1]["payload"]), {})
        self.assertNotIn("test-token-not-real", proc.stdout + proc.stderr)

    def test_failed_registration_is_nonblocking_and_skips_heartbeat(self):
        proc, records = self.run_script(token="test-token-not-real", fail_register=True)
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(len(records), 1)
        self.assertIn("non-blocking", proc.stdout)

if __name__ == "__main__":
    unittest.main()
