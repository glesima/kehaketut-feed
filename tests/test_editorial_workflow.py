import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from editorial_workflow import (
    prepare_draft, revise_draft, select_review_route, public_post_payload
)

class EditorialWorkflowTests(unittest.TestCase):
    def test_no_publication_without_identity_backend(self):
        draft = prepare_draft("Kuntonyrkkeilyn harjoitukset",
                              "Tiistaina kokoonnuttiin salille.",
                              ["fitness"], ["website", "instagram"])
        self.assertEqual(draft.state, "pending_review")
        self.assertFalse(draft.publication_allowed)
        with self.assertRaises(PermissionError):
            public_post_payload(draft)

    def test_multiple_explicit_groups(self):
        draft = prepare_draft("Harjoituskuulumiset", "Kaksi ryhmää mukana.",
                              ["women", "competitive", "women"])
        self.assertEqual(draft.groups, ("competitive", "women"))

    def test_missing_group_not_inferred(self):
        with self.assertRaises(ValueError):
            prepare_draft("Kuvat", "Treeneistä kuvamateriaalia", [])

    def test_invalid_group_rejected(self):
        with self.assertRaises(ValueError):
            prepare_draft("Kuvat", "Treeneistä kuvamateriaalia", ["private-members"])

    def test_invalid_channel_rejected(self):
        with self.assertRaises(ValueError):
            prepare_draft("Kuvat", "Treeneistä kuvamateriaalia", ["juniors"], ["unknown"])

    def test_revision_invalidates_any_prior_signoff(self):
        one = prepare_draft("Uutinen", "Ensimmäinen versio", ["general"])
        two = revise_draft(one, body="Korjattu versio")
        self.assertEqual(one.id, two.id)
        self.assertEqual(two.revision, one.revision+1)
        self.assertNotEqual(one.fingerprint, two.fingerprint)
        self.assertFalse(two.publication_allowed)

    def test_unauthenticated_mail_sender_has_no_approval_route(self):
        self.assertEqual(
            select_review_route(verified_personal_identity=False,
                                is_named_reviewer=True),
            "club_reviewers_shared_queue",
        )
        self.assertEqual(
            select_review_route(verified_personal_identity=True,
                                is_named_reviewer=True),
            "verified_submitter_private_queue",
        )

if __name__ == "__main__":
    unittest.main()
