import pytest
from pen.Pen import Pen


@pytest.fixture
def default_pen():
    return Pen()


@pytest.fixture
def custom_pen():
    return Pen(ink_container_value=500, size_letter=2, color='red')


class TestPenInitialization:
    def test_pen_initialization(self):
        pen = Pen(ink_container_value=100, size_letter=1.5, color='green')
        assert pen.ink_container_value == 100
        assert pen.size_letter == 1.5
        assert pen.color == 'green'


class TestWrite:
    @pytest.mark.parametrize("text,size,expected_remaining", [
        ("hello", 1, 995),
        ("longword", 2, 984),
        ("a" * 1000, 1, 0)
    ])
    def test_write_with_various_ink(self, text, size, expected_remaining):
        pen = Pen(ink_container_value=1000, size_letter=size)
        pen.write(text)
        assert pen.ink_container_value == expected_remaining

    def test_write_empty_string(self, default_pen):
        result = default_pen.write("")
        assert result == ""
        assert default_pen.ink_container_value == 1000

    def test_write_depletes_ink(self):
        pen = Pen(ink_container_value=5, size_letter=1)
        result = pen.write("hello")
        assert result == "hello"
        assert pen.ink_container_value == 0

    def test_write_no_ink(self):
        pen = Pen(ink_container_value=0)
        result = pen.write("hello")
        assert result == ""

    def test_write_partial_word(self):
        pen = Pen(ink_container_value=3, size_letter=1)
        result = pen.write("hello")
        assert result == "hel"
        assert pen.ink_container_value == 0

    @pytest.mark.xfail(reason="size_letter не ограничивает длину слова")
    def test_write_with_large_size_letter(self):
        pen = Pen(ink_container_value=10, size_letter=5)
        result = pen.write("hello")
        assert result == "h"


class TestCheckPenState:
    def test_check_pen_state(self):
        pen = Pen(ink_container_value=5)
        assert pen.check_pen_state() is True
        pen.write("hello")
        assert pen.check_pen_state() is False


class TestGetColor:
    @pytest.mark.xfail(reason="get_color всегда возвращает 'blue'")
    def test_get_color(self):
        pen = Pen(color='red')
        assert pen.get_color() == 'red'


class TestInvalidInputs:
    @pytest.mark.parametrize("ink,size", [
        (None, 1),
        (100, None),
        ("abc", 1)
    ])
    def test_invalid_initialization_raises(self, ink, size):
        with pytest.raises((ValueError, TypeError)):
            Pen(ink_container_value=ink, size_letter=size)

    @pytest.mark.parametrize("ink,size", [
        (-10, 1),
        (100, -1)
    ])
    def test_invalid_initialization_no_exception(self, ink, size):
        pen = Pen(ink_container_value=ink, size_letter=size)
        assert isinstance(pen, Pen)
