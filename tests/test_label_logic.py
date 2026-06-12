from main import get_reading_ease_label

def test_label_returns_very_easy_for_high_score():
    result = get_reading_ease_label(95)
    assert result == "Very Easy"

def test_label_returns_easy_for_medium_high_score():
    result = get_reading_ease_label(75)
    assert result == "Easy"

def test_label_returns_standard_for_medium_score():
    result = get_reading_ease_label(65)
    assert result == "Standard"

def test_label_returns_fairly_difficult_for_low_score():
    result = get_reading_ease_label(55)
    assert result == "Fairly Difficult"

def test_label_returns_difficult_for_medium_low_score():
    result = get_reading_ease_label(40)
    assert result == "Difficult"

def test_label_returns_very_difficult_for_very_low_score():
    result = get_reading_ease_label(20)
    assert result == "Very Difficult"