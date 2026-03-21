"""Tests for kreuzberg-crewai tools."""

from pathlib import Path

import pytest

from kreuzberg_crewai.tools import ExtractInput, KreuzbergExtractMetadataTool, KreuzbergExtractTool, MetadataInput

FIXTURES_DIR = Path(__file__).parent / "fixtures"
SAMPLE_TXT = str(FIXTURES_DIR / "sample.txt")


def test_extract_input_default_output_format() -> None:
    """Default output_format is markdown."""
    schema = ExtractInput(file_path=SAMPLE_TXT)
    assert schema.output_format == "markdown"


def test_extract_input_plain_format() -> None:
    """Accepts plain output format."""
    schema = ExtractInput(file_path=SAMPLE_TXT, output_format="plain")
    assert schema.output_format == "plain"


def test_extract_input_html_format() -> None:
    """Accepts html output format."""
    schema = ExtractInput(file_path=SAMPLE_TXT, output_format="html")
    assert schema.output_format == "html"


def test_extract_input_invalid_format_rejected() -> None:
    """Invalid output_format is rejected by Pydantic."""
    with pytest.raises(Exception):  # noqa: B017, PT011
        ExtractInput(file_path=SAMPLE_TXT, output_format="djot")  # type: ignore[arg-type]


def test_metadata_input_file_path_required() -> None:
    """file_path is required."""
    with pytest.raises(Exception):  # noqa: B017, PT011
        MetadataInput()  # type: ignore[call-arg]


def test_extract_tool_name() -> None:
    """Tool has correct name."""
    tool = KreuzbergExtractTool()
    assert tool.name == "Extract Document"


def test_extract_tool_description() -> None:
    """Tool has a description mentioning format support."""
    tool = KreuzbergExtractTool()
    assert "88+" in tool.description


def test_extract_tool_args_schema() -> None:
    """Tool uses ExtractInput as args schema."""
    tool = KreuzbergExtractTool()
    assert tool.args_schema is ExtractInput


def test_extract_tool_default_markdown() -> None:
    """Default extraction returns markdown content."""
    tool = KreuzbergExtractTool()
    result = tool._run(file_path=SAMPLE_TXT)

    assert isinstance(result, str)
    assert len(result) > 0
    assert "sample document" in result.lower()


def test_extract_tool_plain_format() -> None:
    """Extraction with plain output format returns plain text."""
    tool = KreuzbergExtractTool()
    result = tool._run(file_path=SAMPLE_TXT, output_format="plain")

    assert isinstance(result, str)
    assert "sample document" in result.lower()


def test_extract_tool_html_format() -> None:
    """Extraction with html output format returns HTML."""
    tool = KreuzbergExtractTool()
    result = tool._run(file_path=SAMPLE_TXT, output_format="html")

    assert isinstance(result, str)
    assert len(result) > 0


def test_extract_tool_markdown_preserves_headings() -> None:
    """Markdown output preserves heading structure."""
    tool = KreuzbergExtractTool()
    result = tool._run(file_path=SAMPLE_TXT, output_format="markdown")

    assert "Section One" in result
    assert "Section Two" in result


def test_extract_tool_file_not_found() -> None:
    """OSError propagates for missing files."""
    tool = KreuzbergExtractTool()
    with pytest.raises(OSError, match="does not exist"):
        tool._run(file_path="/nonexistent/path/missing.pdf")


def test_metadata_tool_name() -> None:
    """Tool has correct name."""
    tool = KreuzbergExtractMetadataTool()
    assert tool.name == "Extract Document Metadata"


def test_metadata_tool_description() -> None:
    """Tool has a description mentioning metadata."""
    tool = KreuzbergExtractMetadataTool()
    assert "metadata" in tool.description.lower()


def test_metadata_tool_args_schema() -> None:
    """Tool uses MetadataInput as args schema."""
    tool = KreuzbergExtractMetadataTool()
    assert tool.args_schema is MetadataInput


def test_metadata_tool_returns_string() -> None:
    """Metadata extraction returns a string."""
    tool = KreuzbergExtractMetadataTool()
    result = tool._run(file_path=SAMPLE_TXT)

    assert isinstance(result, str)


def test_metadata_tool_contains_format_type() -> None:
    """Metadata includes format_type field."""
    tool = KreuzbergExtractMetadataTool()
    result = tool._run(file_path=SAMPLE_TXT)

    assert "format_type" in result


def test_metadata_tool_file_not_found() -> None:
    """OSError propagates for missing files."""
    tool = KreuzbergExtractMetadataTool()
    with pytest.raises(OSError, match="does not exist"):
        tool._run(file_path="/nonexistent/path/missing.pdf")
