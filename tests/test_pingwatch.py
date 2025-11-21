import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import pingwatch

# Test de la fonction load_urls_from_file
def test_load_urls_from_file(tmp_path: Path):
    file = tmp_path / "urls.txt"
    file.write_text(
        """
        https://example.com
        # commentaire
        https://google.com

        """,
        encoding="utf-8",
    )

    urls = pingwatch.load_urls_from_file(str(file))
    assert urls == ["https://example.com", "https://google.com"]

# Test de la fonction check_url
def test_main_without_urls(monkeypatch, capsys):
    # Simule une exécution sans arguments
    exit_code = pingwatch.main([])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Aucune URL fournie" in captured.out
