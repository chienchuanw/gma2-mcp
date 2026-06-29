"""Tests for grandMA2 RDM keywords."""


class TestRdm:
    def test_rdm_automatch(self):
        from src.commands import rdm_automatch

        assert rdm_automatch() == "rdmautomatch"

    def test_rdm_autopatch(self):
        from src.commands import rdm_autopatch

        assert rdm_autopatch() == "rdmautopatch"

    def test_rdm_fixture_type(self):
        from src.commands import rdm_fixture_type

        assert rdm_fixture_type() == "rdmfixturetype"

    def test_rdm_info(self):
        from src.commands import rdm_info

        assert rdm_info() == "rdminfo"

    def test_rdm_list(self):
        from src.commands import rdm_list

        assert rdm_list() == "rdmlist"

    def test_rdm_set_parameter(self):
        from src.commands import rdm_set_parameter

        assert rdm_set_parameter() == "rdmsetparameter"

    def test_rdm_setpatch(self):
        from src.commands import rdm_setpatch

        assert rdm_setpatch() == "rdmsetpatch"

    def test_rdm_unmatch(self):
        from src.commands import rdm_unmatch

        assert rdm_unmatch() == "rdmunmatch"
