"""Public documentation checks; no deployment or private-media access."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ContextHandoffTests(unittest.TestCase):
    def test_public_entrypoint_is_linked(self):
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        handoff = (ROOT / 'CONTEXT_HANDOFF.md').read_text(encoding='utf-8')
        self.assertIn('CONTEXT_HANDOFF.md', readme)
        for required in ('CURRENT_STATUS.md', 'PUBLIC_SCOPE.md', 'yksityinen'):
            self.assertIn(required, handoff)

    def test_status_separates_receipt_from_publishing(self):
        status = (ROOT / 'CURRENT_STATUS.md').read_text(encoding='utf-8')
        self.assertIn('28.10.2026', status)
        self.assertIn('receive-only', status)
        self.assertIn('Kolme kilpailuvideokokonaisuutta', status)
        self.assertIn('Ei vielä tuotantokäytössä kokonaisuutena', status)

    def test_new_public_docs_do_not_include_private_operational_values(self):
        for name in ('CURRENT_STATUS.md', 'CONTEXT_HANDOFF.md'):
            text = (ROOT / name).read_text(encoding='utf-8')
            for private_value in ('/mnt/storage/', 'dropbox.private.json',
                                  'dropbox.com/request/', 'refresh_token',
                                  'Authorization: Bearer'):
                self.assertNotIn(private_value, text)


if __name__ == '__main__':
    unittest.main()
