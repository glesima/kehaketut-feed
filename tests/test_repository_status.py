"""Small documentation regressions; not a secret scan or deployment test."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RepositoryStatusTests(unittest.TestCase):
    def test_readme_points_to_current_status(self):
        text = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('CURRENT_STATUS.md', text)
        self.assertIn('PUBLIC_SCOPE.md', text)
        self.assertNotIn('32 s videopilotti (ei julkaistu)', text)

    def test_current_status_distinguishes_missing_pipeline(self):
        text = (ROOT / 'CURRENT_STATUS.md').read_text(encoding='utf-8')
        self.assertIn('Ei vielä tuotantokäytössä kokonaisuutena', text)
        self.assertIn('SHA-256', text)
        self.assertIn('40395207746', text)

    def test_ignore_covers_common_private_runtime_artifacts(self):
        patterns = set((ROOT / '.gitignore').read_text().splitlines())
        for value in ['*.mp4', '*.mov', '*.sqlite', '*.sqlite-*', '*.pem',
                      '*.key', 'incoming/', 'handoff/', '.env']:
            self.assertIn(value, patterns)

    def test_public_scope_covers_non_file_surfaces(self):
        text = (ROOT / 'PUBLIC_SCOPE.md').read_text(encoding='utf-8')
        for value in ['issueita', 'PR-kuvauksia', 'GitHub Actions', 'historiasta']:
            self.assertIn(value, text)


if __name__ == '__main__':
    unittest.main()
