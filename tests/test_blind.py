"""
Blind and Preview Keywords Tests

Tests for grandMA2 Blind, BlindEdit, Preview, and PreviewEdit
function keyword command generation.

Blind keyword:
- Toggles blind mode (edits not visible on stage output)
- Can target specific executors

Preview keyword:
- Toggles preview mode (visualize executor output without affecting stage)
- Can target specific executors

Test Classes:
- TestBlind: Tests for Blind command generation
- TestBlindEdit: Tests for BlindEdit command generation
- TestPreview: Tests for Preview command generation
- TestPreviewEdit: Tests for PreviewEdit command generation
"""


class TestBlind:
    """
    Tests for Blind keyword - toggles blind editing mode.

    Syntax:
        Blind
        Blind [Object]
    """

    def test_blind_no_args(self):
        """Test blind with no arguments: blind"""
        from src.commands import blind

        result = blind()
        assert result == "blind"

    def test_blind_executor(self):
        """Test blind executor: blind executor 3"""
        from src.commands import blind

        result = blind("executor 3")
        assert result == "blind executor 3"


class TestBlindEdit:
    """
    Tests for BlindEdit keyword - toggles blind edit mode.

    Syntax:
        BlindEdit
    """

    def test_blind_edit_no_args(self):
        """Test blindedit with no arguments: blindedit"""
        from src.commands import blind_edit

        result = blind_edit()
        assert result == "blindedit"


class TestPreview:
    """
    Tests for Preview keyword - toggles preview mode.

    Syntax:
        Preview
        Preview [Object]
    """

    def test_preview_no_args(self):
        """Test preview with no arguments: preview"""
        from src.commands import preview

        result = preview()
        assert result == "preview"

    def test_preview_executor(self):
        """Test preview executor: preview executor 5"""
        from src.commands import preview

        result = preview("executor 5")
        assert result == "preview executor 5"


class TestPreviewEdit:
    """
    Tests for PreviewEdit keyword - toggles preview edit mode.

    Syntax:
        PreviewEdit
    """

    def test_preview_edit_no_args(self):
        """Test previewedit with no arguments: previewedit"""
        from src.commands import preview_edit

        result = preview_edit()
        assert result == "previewedit"
