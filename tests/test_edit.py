"""
Edit Commands Tests

Tests for grandMA2 edit operation command generation.
Includes Copy, Move, Delete, and Remove command series.

Test Classes:
- TestCopyCommands: Tests for copy, copy_cue
- TestMoveCommands: Tests for move
- TestDeleteCommands: Tests for delete series
- TestRemoveCommands: Tests for remove series
"""

import pytest


class TestCopyCommands:
    """Tests for Copy keyword commands."""

    # ---- Basic Copy ----

    def test_copy_single_to_target(self):
        """Test copy single object: copy group 1 at 5"""
        from src.commands import copy

        result = copy("group", 1, 5)
        assert result == "copy group 1 at 5"

    def test_copy_cue_to_target(self):
        """Test copy cue: copy cue 2 at 6"""
        from src.commands import copy

        result = copy("cue", 2, 6)
        assert result == "copy cue 2 at 6"

    def test_copy_macro_to_target(self):
        """Test copy macro: copy macro 2 at 6"""
        from src.commands import copy

        result = copy("macro", 2, 6)
        assert result == "copy macro 2 at 6"

    # ---- Copy to Clipboard ----

    def test_copy_to_clipboard(self):
        """Test copy to clipboard: copy cue 5"""
        from src.commands import copy

        result = copy("cue", 5)
        assert result == "copy cue 5"

    def test_copy_cue_to_clipboard(self):
        """Test copy_cue to clipboard: copy cue 5"""
        from src.commands import copy_cue

        result = copy_cue(5)
        assert result == "copy cue 5"

    # ---- Copy with Range (Thru) ----

    def test_copy_range_to_target(self):
        """Test copy range: copy group 1 thru 3 at 11"""
        from src.commands import copy

        result = copy("group", 1, 11, end=3)
        assert result == "copy group 1 thru 3 at 11"

    def test_copy_to_target_range(self):
        """Test copy to target range: copy group 2 at 6 thru 8"""
        from src.commands import copy

        result = copy("group", 2, 6, target_end=8)
        assert result == "copy group 2 at 6 thru 8"

    # ---- Copy with List ----

    def test_copy_list_to_target(self):
        """Test copy list: copy group 1 + 3 + 5 at 10"""
        from src.commands import copy

        result = copy("group", [1, 3, 5], 10)
        assert result == "copy group 1 + 3 + 5 at 10"

    def test_copy_to_target_list(self):
        """Test copy to target list: copy group 1 at 5 + 6 + 7"""
        from src.commands import copy

        result = copy("group", 1, [5, 6, 7])
        assert result == "copy group 1 at 5 + 6 + 7"

    # ---- Copy with Options ----

    def test_copy_with_overwrite(self):
        """Test copy with overwrite option."""
        from src.commands import copy

        result = copy("group", 1, 5, overwrite=True)
        assert result == "copy group 1 at 5 /overwrite"

    def test_copy_with_merge(self):
        """Test copy with merge option."""
        from src.commands import copy

        result = copy("cue", 1, 5, merge=True)
        assert result == "copy cue 1 at 5 /merge"

    def test_copy_with_noconfirm(self):
        """Test copy with noconfirm option."""
        from src.commands import copy

        result = copy("macro", 1, 5, noconfirm=True)
        assert result == "copy macro 1 at 5 /noconfirm"

    def test_copy_with_status(self):
        """Test copy with status option."""
        from src.commands import copy

        result = copy("cue", 1, 5, status=True)
        assert result == "copy cue 1 at 5 /status=true"

    def test_copy_with_cueonly(self):
        """Test copy with cueonly option."""
        from src.commands import copy

        result = copy("cue", 1, 5, cueonly=True)
        assert result == "copy cue 1 at 5 /cueonly=true"

    def test_copy_with_multiple_options(self):
        """Test copy with multiple options."""
        from src.commands import copy

        result = copy("cue", 1, 5, merge=True, noconfirm=True)
        assert result == "copy cue 1 at 5 /merge /noconfirm"

    # ---- copy_cue Convenience Function ----

    def test_copy_cue_basic(self):
        """Test copy_cue convenience function."""
        from src.commands import copy_cue

        result = copy_cue(2, 6)
        assert result == "copy cue 2 at 6"

    def test_copy_cue_with_range(self):
        """Test copy_cue with range."""
        from src.commands import copy_cue

        result = copy_cue(1, 10, end=5)
        assert result == "copy cue 1 thru 5 at 10"

    def test_copy_cue_with_options(self):
        """Test copy_cue with options."""
        from src.commands import copy_cue

        result = copy_cue(1, 10, overwrite=True, noconfirm=True)
        assert result == "copy cue 1 at 10 /overwrite /noconfirm"


class TestMoveCommands:
    """Tests for Move keyword commands."""

    # ---- Basic Move ----

    def test_move_single(self):
        """Test move single object: move group 5 at 9"""
        from src.commands import move

        result = move("group", 5, 9)
        assert result == "move group 5 at 9"

    def test_move_cue(self):
        """Test move cue: move cue 5 at 1"""
        from src.commands import move

        result = move("cue", 5, 1)
        assert result == "move cue 5 at 1"

    def test_move_preset(self):
        """Test move preset: move preset 3 at 10"""
        from src.commands import move

        result = move("preset", 3, 10)
        assert result == "move preset 3 at 10"

    # ---- Move with Range (Thru) ----

    def test_move_range(self):
        """Test move range: move group 1 thru 3 at 10"""
        from src.commands import move

        result = move("group", 1, 10, end=3)
        assert result == "move group 1 thru 3 at 10"

    def test_move_to_target_range(self):
        """Test move to target range: move group 1 at 10 thru 12"""
        from src.commands import move

        result = move("group", 1, 10, target_end=12)
        assert result == "move group 1 at 10 thru 12"

    # ---- Move with List ----

    def test_move_list_to_list(self):
        """Test move list to list: move preset 1 + 3 + 5 at 10 + 12 + 14"""
        from src.commands import move

        result = move("preset", [1, 3, 5], [10, 12, 14])
        assert result == "move preset 1 + 3 + 5 at 10 + 12 + 14"

    def test_move_list_to_single(self):
        """Test move list to single target: move group 1 + 2 + 3 at 10"""
        from src.commands import move

        result = move("group", [1, 2, 3], 10)
        assert result == "move group 1 + 2 + 3 at 10"


class TestDeleteCommands:
    """Tests for Delete keyword commands."""

    # ---- Generic Delete ----

    def test_delete_generic(self):
        """Test generic delete: delete cue 7"""
        from src.commands import delete

        result = delete("cue", 7)
        assert result == "delete cue 7"

    def test_delete_group(self):
        """Test delete group: delete group 3"""
        from src.commands import delete

        result = delete("group", 3)
        assert result == "delete group 3"

    def test_delete_fixture(self):
        """Test delete fixture (unpatch): delete fixture 4"""
        from src.commands import delete

        result = delete("fixture", 4)
        assert result == "delete fixture 4"

    def test_delete_world(self):
        """Test delete world: delete world 6"""
        from src.commands import delete

        result = delete("world", 6)
        assert result == "delete world 6"

    def test_delete_range(self):
        """Test delete range: delete cue 1 thru 5"""
        from src.commands import delete

        result = delete("cue", 1, end=5)
        assert result == "delete cue 1 thru 5"

    def test_delete_list(self):
        """Test delete list: delete group 1 + 3 + 5"""
        from src.commands import delete

        result = delete("group", [1, 3, 5])
        assert result == "delete group 1 + 3 + 5"

    def test_delete_with_noconfirm(self):
        """Test delete with noconfirm option."""
        from src.commands import delete

        result = delete("cue", 1, end=5, noconfirm=True)
        assert result == "delete cue 1 thru 5 /noconfirm"

    def test_delete_with_cueonly(self):
        """Test delete with cueonly option."""
        from src.commands import delete

        result = delete("cue", 3, cueonly=True)
        assert result == "delete cue 3 /cueonly"

    def test_delete_with_multiple_options(self):
        """Test delete with multiple options."""
        from src.commands import delete

        result = delete("cue", 1, deletevalues=True, cueonly=True, noconfirm=True)
        assert result == "delete cue 1 /deletevalues /cueonly /noconfirm"

    def test_delete_with_selection_filter(self):
        """Test delete with selection filter."""
        from src.commands import delete

        result = delete("cue", 5, selection_filter="fixture 1 thru 10")
        assert result == "delete cue 5 fixture 1 thru 10"

    # ---- Delete Cue Convenience ----

    def test_delete_cue_basic(self):
        """Test delete cue: delete cue 7"""
        from src.commands import delete_cue

        result = delete_cue(7)
        assert result == "delete cue 7"

    def test_delete_cue_with_sequence(self):
        """Test delete cue with sequence: delete cue 1 sequence 2"""
        from src.commands import delete_cue

        result = delete_cue(1, sequence_id=2)
        assert result == "delete cue 1 sequence 2"

    def test_delete_cue_range(self):
        """Test delete cue range: delete cue 1 thru 5"""
        from src.commands import delete_cue

        result = delete_cue(1, end=5)
        assert result == "delete cue 1 thru 5"

    def test_delete_cue_with_options(self):
        """Test delete cue with options."""
        from src.commands import delete_cue

        result = delete_cue(1, end=5, deletevalues=True, noconfirm=True)
        assert result == "delete cue 1 thru 5 /deletevalues /noconfirm"

    # ---- Delete Group Convenience ----

    def test_delete_group_basic(self):
        """Test delete group basic: delete group 3"""
        from src.commands import delete_group

        result = delete_group(3)
        assert result == "delete group 3"

    def test_delete_group_range(self):
        """Test delete group range: delete group 1 thru 5"""
        from src.commands import delete_group

        result = delete_group(1, end=5)
        assert result == "delete group 1 thru 5"

    def test_delete_group_with_noconfirm(self):
        """Test delete group with noconfirm."""
        from src.commands import delete_group

        result = delete_group(1, noconfirm=True)
        assert result == "delete group 1 /noconfirm"

    # ---- Delete Preset Convenience ----

    def test_delete_preset_by_name(self):
        """Test delete preset by name: delete preset 2.5 (color = presettype 2)"""
        from src.commands import delete_preset

        result = delete_preset("color", 5)
        assert result == "delete preset 2.5"

    def test_delete_preset_by_number(self):
        """Test delete preset by number: delete preset 1.1"""
        from src.commands import delete_preset

        result = delete_preset(1, 1)
        assert result == "delete preset 1.1"

    def test_delete_preset_range(self):
        """Test delete preset range: delete preset 1.1 thru 10"""
        from src.commands import delete_preset

        result = delete_preset(1, 1, end=10)
        assert result == "delete preset 1.1 thru 10"

    # ---- Delete Fixture Convenience ----

    def test_delete_fixture_basic(self):
        """Test delete fixture (unpatch): delete fixture 4"""
        from src.commands import delete_fixture

        result = delete_fixture(4)
        assert result == "delete fixture 4"

    def test_delete_fixture_range(self):
        """Test delete fixture range: delete fixture 1 thru 10"""
        from src.commands import delete_fixture

        result = delete_fixture(1, end=10)
        assert result == "delete fixture 1 thru 10"

    def test_delete_fixture_list(self):
        """Test delete fixture list: delete fixture 1 + 5 + 10"""
        from src.commands import delete_fixture

        result = delete_fixture([1, 5, 10])
        assert result == "delete fixture 1 + 5 + 10"

    # ---- Delete Messages ----

    def test_delete_messages(self):
        """Test delete messages: delete messages"""
        from src.commands import delete_messages

        result = delete_messages()
        assert result == "delete messages"


class TestRemoveCommands:
    """Tests for Remove keyword commands."""

    # ---- Generic Remove ----

    def test_remove_basic(self):
        """Test basic remove: remove"""
        from src.commands import remove

        result = remove()
        assert result == "remove"

    def test_remove_selection(self):
        """Test remove selection: remove selection"""
        from src.commands import remove

        result = remove("selection")
        assert result == "remove selection"

    def test_remove_fixture_with_id(self):
        """Test remove fixture: remove fixture 1"""
        from src.commands import remove

        result = remove("fixture", 1)
        assert result == "remove fixture 1"

    def test_remove_with_range(self):
        """Test remove with range: remove fixture 1 thru 10"""
        from src.commands import remove

        result = remove("fixture", 1, end=10)
        assert result == "remove fixture 1 thru 10"

    def test_remove_with_if_filter(self):
        """Test remove with if filter: remove fixture 1 if PresetType 1"""
        from src.commands import remove

        result = remove("fixture", 1, if_filter="PresetType 1")
        assert result == "remove fixture 1 if PresetType 1"

    def test_remove_presettype_quoted(self):
        """Test remove presettype: remove presettype "position" """
        from src.commands import remove

        result = remove("presettype", '"position"')
        assert result == 'remove presettype "position"'

    # ---- Remove Selection Convenience ----

    def test_remove_selection_convenience(self):
        """Test remove selection convenience: remove selection"""
        from src.commands import remove_selection

        result = remove_selection()
        assert result == "remove selection"

    # ---- Remove Preset Type Convenience ----

    def test_remove_preset_type_by_name(self):
        """Test remove preset type by name: remove presettype "position" """
        from src.commands import remove_preset_type

        result = remove_preset_type("position")
        assert result == 'remove presettype "position"'

    def test_remove_preset_type_by_number(self):
        """Test remove preset type by number: remove presettype 1"""
        from src.commands import remove_preset_type

        result = remove_preset_type(1)
        assert result == "remove presettype 1"

    def test_remove_preset_type_with_filter(self):
        """Test remove preset type with filter."""
        from src.commands import remove_preset_type

        result = remove_preset_type("color", if_filter="fixture 1 thru 10")
        assert result == 'remove presettype "color" if fixture 1 thru 10'

    # ---- Remove Fixture Convenience ----

    def test_remove_fixture_basic(self):
        """Test remove fixture: remove fixture 1"""
        from src.commands import remove_fixture

        result = remove_fixture(1)
        assert result == "remove fixture 1"

    def test_remove_fixture_range(self):
        """Test remove fixture range: remove fixture 1 thru 10"""
        from src.commands import remove_fixture

        result = remove_fixture(1, end=10)
        assert result == "remove fixture 1 thru 10"

    def test_remove_fixture_list(self):
        """Test remove fixture list: remove fixture 1 + 5 + 10"""
        from src.commands import remove_fixture

        result = remove_fixture([1, 5, 10])
        assert result == "remove fixture 1 + 5 + 10"

    def test_remove_fixture_with_if_filter(self):
        """Test remove fixture with if filter."""
        from src.commands import remove_fixture

        result = remove_fixture(1, if_filter="PresetType 1")
        assert result == "remove fixture 1 if PresetType 1"

    # ---- Remove Effect Convenience ----

    def test_remove_effect_basic(self):
        """Test remove effect: remove effect 1"""
        from src.commands import remove_effect

        result = remove_effect(1)
        assert result == "remove effect 1"

    def test_remove_effect_range(self):
        """Test remove effect range: remove effect 1 thru 5"""
        from src.commands import remove_effect

        result = remove_effect(1, end=5)
        assert result == "remove effect 1 thru 5"
