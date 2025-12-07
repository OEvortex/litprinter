#!/usr/bin/env python3
"""
LitPrinter Text Module

Provides a Text class for handling styled text with spans.
Inspired by Rich's Text class with support for markup, styling ranges, and rendering.

Author: OEvortex <helpingai5@gmail.com>
License: MIT
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Iterator, Union, Callable, Pattern, TYPE_CHECKING
import textwrap

if TYPE_CHECKING:
    from .style import Style


@dataclass
class Span:
    """Represents a styled span of text.
    
    A span defines a range of characters and the style applied to them.
    Multiple spans can overlap, with later spans taking precedence.
    
    Attributes:
        start: Start index (inclusive).
        end: End index (exclusive).
        style: Style string to apply.
    """
    start: int
    end: int
    style: str
    
    def __repr__(self) -> str:
        return f"Span({self.start}, {self.end}, {self.style!r})"
    
    def __bool__(self) -> bool:
        return self.end > self.start
    
    def move(self, offset: int) -> "Span":
        """Move span by offset.
        
        Args:
            offset: Amount to move start and end.
            
        Returns:
            New Span with adjusted positions.
        """
        return Span(self.start + offset, self.end + offset, self.style)
    
    def extend(self, cells: int) -> "Span":
        """Extend span by cells.
        
        Args:
            cells: Number of cells to extend end by.
            
        Returns:
            New Span with extended end.
        """
        return Span(self.start, self.end + cells, self.style)
    
    def crop(self, start: int, end: int) -> Optional["Span"]:
        """Crop span to a range.
        
        Args:
            start: Start of range.
            end: End of range.
            
        Returns:
            Cropped Span, or None if completely outside range.
        """
        new_start = max(self.start, start)
        new_end = min(self.end, end)
        if new_end <= new_start:
            return None
        return Span(new_start - start, new_end - start, self.style)


class Text:
    """A string with associated spans of styles.
    
    The Text class provides methods for building up styled text from
    multiple parts, applying styles to ranges, and rendering the
    final output with ANSI codes.
    
    Example:
        >>> text = Text("Hello, World!")
        >>> text.stylize("bold", 0, 5)
        >>> text.stylize("red", 7, 12)
        >>> print(text.render())
        # Prints "Hello" in bold and "World" in red
    
    Attributes:
        _text: The plain text content.
        _spans: List of styled spans.
        style: Default style for the text.
        no_wrap: Whether to disable text wrapping.
        overflow: Overflow handling method.
        tab_size: Number of spaces per tab.
    """
    
    def __init__(
        self,
        text: str = "",
        style: Optional[str] = None,
        *,
        no_wrap: bool = False,
        overflow: str = "fold",
        tab_size: int = 8,
    ):
        """Initialize a Text object.
        
        Args:
            text: Initial text content.
            style: Optional default style.
            no_wrap: Whether to disable text wrapping.
            overflow: Overflow handling ("fold", "ellipsis", "crop").
            tab_size: Number of spaces per tab.
        """
        self._text = str(text)
        self._spans: List[Span] = []
        self.style = style
        self.no_wrap = no_wrap
        self.overflow = overflow
        self.tab_size = tab_size
        
        # Apply default style if provided
        if style and self._text:
            self._spans.append(Span(0, len(self._text), style))
    
    def __repr__(self) -> str:
        return f"Text({self._text!r}, style={self.style!r})"
    
    def __str__(self) -> str:
        return self._text
    
    def __len__(self) -> int:
        return len(self._text)
    
    def __bool__(self) -> bool:
        return bool(self._text)
    
    def __add__(self, other: Union["Text", str]) -> "Text":
        """Concatenate with another Text or string."""
        if isinstance(other, str):
            other = Text(other)
        result = self.copy()
        result.append_text(other)
        return result
    
    def __radd__(self, other: str) -> "Text":
        """Right concatenation with string."""
        if isinstance(other, str):
            result = Text(other)
            result.append_text(self)
            return result
        return NotImplemented
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Text):
            return self._text == other._text and self._spans == other._spans
        if isinstance(other, str):
            return self._text == other
        return False
    
    def __contains__(self, other: str) -> bool:
        return other in self._text
    
    def __getitem__(self, slice_obj: slice) -> "Text":
        """Slice the text."""
        text = self._text[slice_obj]
        result = Text(text, no_wrap=self.no_wrap, overflow=self.overflow, tab_size=self.tab_size)
        
        start = slice_obj.start or 0
        stop = slice_obj.stop if slice_obj.stop is not None else len(self._text)
        
        for span in self._spans:
            cropped = span.crop(start, stop)
            if cropped:
                result._spans.append(cropped)
        
        return result
    
    @property
    def plain(self) -> str:
        """Get the plain text without styling.
        
        Returns:
            The raw text content.
        """
        return self._text
    
    @plain.setter
    def plain(self, value: str) -> None:
        """Set the plain text, clearing spans.
        
        Args:
            value: New text content.
        """
        self._text = value
        self._spans.clear()
    
    @property
    def spans(self) -> List[Span]:
        """Get the list of spans.
        
        Returns:
            List of Span objects.
        """
        return self._spans
    
    @property
    def cell_length(self) -> int:
        """Get the display width of the text.
        
        Returns:
            Number of cells the text occupies.
        """
        # For now, assume 1 cell per character
        # Could be enhanced for wide characters
        return len(self._text)
    
    def copy(self) -> "Text":
        """Create a copy of this Text.
        
        Returns:
            A new Text with the same content and spans.
        """
        result = Text(
            self._text,
            no_wrap=self.no_wrap,
            overflow=self.overflow,
            tab_size=self.tab_size,
        )
        result._spans = [Span(s.start, s.end, s.style) for s in self._spans]
        result.style = self.style
        return result
    
    def append(self, text: Union[str, "Text"], style: Optional[str] = None) -> "Text":
        """Append text with optional style.
        
        Args:
            text: Text to append.
            style: Optional style to apply.
            
        Returns:
            Self for chaining.
        """
        if isinstance(text, Text):
            self.append_text(text)
            return self
        
        start = len(self._text)
        self._text += text
        
        if style:
            self._spans.append(Span(start, len(self._text), style))
        
        return self
    
    def append_text(self, text: "Text") -> "Text":
        """Append another Text object.
        
        Args:
            text: Text object to append.
            
        Returns:
            Self for chaining.
        """
        offset = len(self._text)
        self._text += text._text
        
        for span in text._spans:
            self._spans.append(span.move(offset))
        
        return self
    
    def stylize(
        self,
        style: str,
        start: int = 0,
        end: Optional[int] = None,
    ) -> "Text":
        """Apply a style to a range of text.
        
        Args:
            style: Style string to apply.
            start: Start index (inclusive).
            end: End index (exclusive), or None for end of text.
            
        Returns:
            Self for chaining.
        """
        if end is None:
            end = len(self._text)
        
        if start < 0:
            start = len(self._text) + start
        if end < 0:
            end = len(self._text) + end
        
        start = max(0, start)
        end = min(len(self._text), end)
        
        if end > start:
            self._spans.append(Span(start, end, style))
        
        return self
    
    def stylize_all(self, style: str) -> "Text":
        """Apply a style to all text.
        
        Args:
            style: Style string to apply.
            
        Returns:
            Self for chaining.
        """
        return self.stylize(style, 0, len(self._text))
    
    def highlight_words(
        self,
        words: Union[str, List[str]],
        style: str,
        *,
        case_sensitive: bool = True,
    ) -> "Text":
        """Highlight matching words with a style.
        
        Args:
            words: Word or list of words to highlight.
            style: Style to apply.
            case_sensitive: Whether matching is case-sensitive.
            
        Returns:
            Self for chaining.
        """
        if isinstance(words, str):
            words = [words]
        
        text = self._text
        if not case_sensitive:
            text = text.lower()
        
        for word in words:
            search_word = word if case_sensitive else word.lower()
            start = 0
            while True:
                pos = text.find(search_word, start)
                if pos == -1:
                    break
                self.stylize(style, pos, pos + len(word))
                start = pos + 1
        
        return self
    
    def highlight_regex(
        self,
        pattern: Union[str, Pattern],
        style: str,
    ) -> "Text":
        """Highlight text matching a regex pattern.
        
        Args:
            pattern: Regex pattern to match.
            style: Style to apply to matches.
            
        Returns:
            Self for chaining.
        """
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        
        for match in pattern.finditer(self._text):
            self.stylize(style, match.start(), match.end())
        
        return self
    
    def split(
        self,
        separator: str = "\n",
        include_separator: bool = False,
    ) -> List["Text"]:
        """Split text at separator.
        
        Args:
            separator: String to split at.
            include_separator: Whether to include separator in results.
            
        Returns:
            List of Text objects.
        """
        results = []
        parts = self._text.split(separator)
        current_pos = 0
        
        for i, part in enumerate(parts):
            end_pos = current_pos + len(part)
            text = Text(
                part,
                no_wrap=self.no_wrap,
                overflow=self.overflow,
                tab_size=self.tab_size,
            )
            
            for span in self._spans:
                cropped = span.crop(current_pos, end_pos)
                if cropped:
                    text._spans.append(cropped)
            
            results.append(text)
            
            if include_separator and i < len(parts) - 1:
                sep_text = Text(separator)
                results.append(sep_text)
            
            current_pos = end_pos + len(separator)
        
        return results
    
    def join(self, texts: List["Text"]) -> "Text":
        """Join texts with this text as separator.
        
        Args:
            texts: List of Text objects to join.
            
        Returns:
            New Text with all texts joined.
        """
        if not texts:
            return Text()
        
        result = texts[0].copy()
        for text in texts[1:]:
            result.append_text(self.copy())
            result.append_text(text)
        
        return result
    
    def wrap(
        self,
        width: int,
        justify: str = "left",
        overflow: Optional[str] = None,
    ) -> List["Text"]:
        """Wrap text to a given width.
        
        Args:
            width: Maximum line width.
            justify: Justification ("left", "center", "right", "full").
            overflow: Overflow handling, defaults to self.overflow.
            
        Returns:
            List of Text lines.
        """
        if overflow is None:
            overflow = self.overflow
        
        if self.no_wrap or width <= 0:
            return [self.copy()]
        
        wrapped_lines = textwrap.wrap(
            self._text,
            width=width,
            expand_tabs=False,
            replace_whitespace=False,
            break_long_words=True,
            break_on_hyphens=True,
        )
        
        if not wrapped_lines:
            return [Text()]
        
        results = []
        current_pos = 0
        
        for line in wrapped_lines:
            # Find position of this line in original text
            start = self._text.find(line, current_pos)
            if start == -1:
                start = current_pos
            end = start + len(line)
            
            text = Text(
                line,
                no_wrap=self.no_wrap,
                overflow=self.overflow,
                tab_size=self.tab_size,
            )
            
            for span in self._spans:
                cropped = span.crop(start, end)
                if cropped:
                    text._spans.append(cropped)
            
            results.append(text)
            current_pos = end
        
        return results
    
    def fit(self, width: int) -> "Text":
        """Truncate text to fit within width.
        
        Args:
            width: Maximum width.
            
        Returns:
            Truncated Text.
        """
        if len(self._text) <= width:
            return self.copy()
        
        if width <= 3:
            return Text("." * width)
        
        truncated = self._text[:width - 3] + "..."
        result = Text(
            truncated,
            no_wrap=self.no_wrap,
            overflow=self.overflow,
            tab_size=self.tab_size,
        )
        
        for span in self._spans:
            cropped = span.crop(0, width - 3)
            if cropped:
                result._spans.append(cropped)
        
        return result
    
    def pad_left(self, width: int, character: str = " ") -> "Text":
        """Pad text on the left.
        
        Args:
            width: Total width after padding.
            character: Character to use for padding.
            
        Returns:
            New Text with padding.
        """
        padding = max(0, width - len(self._text))
        if padding == 0:
            return self.copy()
        
        result = Text(character * padding)
        result.append_text(self)
        return result
    
    def pad_right(self, width: int, character: str = " ") -> "Text":
        """Pad text on the right.
        
        Args:
            width: Total width after padding.
            character: Character to use for padding.
            
        Returns:
            New Text with padding.
        """
        padding = max(0, width - len(self._text))
        if padding == 0:
            return self.copy()
        
        result = self.copy()
        result.append(character * padding)
        return result
    
    def center(self, width: int, character: str = " ") -> "Text":
        """Center text within width.
        
        Args:
            width: Total width.
            character: Character to use for padding.
            
        Returns:
            New centered Text.
        """
        padding = max(0, width - len(self._text))
        if padding == 0:
            return self.copy()
        
        left_pad = padding // 2
        right_pad = padding - left_pad
        
        result = Text(character * left_pad)
        result.append_text(self)
        result.append(character * right_pad)
        return result
    
    def expand_tabs(self) -> "Text":
        """Expand tabs to spaces.
        
        Returns:
            New Text with tabs expanded.
        """
        if "\t" not in self._text:
            return self.copy()
        
        result = Text(
            self._text.expandtabs(self.tab_size),
            no_wrap=self.no_wrap,
            overflow=self.overflow,
            tab_size=self.tab_size,
        )
        # Note: This doesn't properly adjust spans for tab expansion
        # A more sophisticated implementation would be needed
        return result
    
    def strip(self) -> "Text":
        """Strip whitespace from both ends.
        
        Returns:
            New Text with whitespace stripped.
        """
        stripped = self._text.strip()
        if stripped == self._text:
            return self.copy()
        
        start = len(self._text) - len(self._text.lstrip())
        end = start + len(stripped)
        
        return self[start:end]
    
    def lstrip(self) -> "Text":
        """Strip whitespace from left.
        
        Returns:
            New Text with left whitespace stripped.
        """
        stripped = self._text.lstrip()
        if stripped == self._text:
            return self.copy()
        
        start = len(self._text) - len(stripped)
        return self[start:]
    
    def rstrip(self) -> "Text":
        """Strip whitespace from right.
        
        Returns:
            New Text with right whitespace stripped.
        """
        stripped = self._text.rstrip()
        if stripped == self._text:
            return self.copy()
        
        return self[:len(stripped)]
    
    def render(self) -> str:
        """Render the text with ANSI styling.
        
        Returns:
            Text with ANSI escape codes applied.
        """
        from .style import Style
        from .colors import Colors
        
        if not self._spans:
            return self._text
        
        # Sort spans by start position, then by end position (reverse)
        # This ensures proper nesting
        sorted_spans = sorted(self._spans, key=lambda s: (s.start, -s.end))
        
        # Build result character by character
        result = []
        active_styles: List[Tuple[int, str]] = []  # (end_pos, style)
        
        for i, char in enumerate(self._text):
            # Remove styles that have ended
            active_styles = [(end, s) for end, s in active_styles if end > i]
            
            # Add new styles that start at this position
            for span in sorted_spans:
                if span.start == i:
                    active_styles.append((span.end, span.style))
            
            # Apply all active styles to character
            if active_styles:
                combined_style = " ".join(s for _, s in active_styles)
                styled_char = Style.parse(combined_style).render(char)
                result.append(styled_char)
            else:
                result.append(char)
        
        return "".join(result)
    
    def render_segments(self) -> List["Segment"]:
        """Render the text as a list of Segments.
        
        Returns:
            List of Segment objects.
        """
        from .segment import Segment
        
        if not self._spans:
            return [Segment(self._text)]
        
        # Build segments by calculating style at each change point
        change_points = {0, len(self._text)}
        for span in self._spans:
            change_points.add(span.start)
            change_points.add(span.end)
        
        points = sorted(change_points)
        segments = []
        
        for i in range(len(points) - 1):
            start = points[i]
            end = points[i + 1]
            text = self._text[start:end]
            
            if not text:
                continue
            
            # Find all active styles at this position
            active_styles = []
            for span in self._spans:
                if span.start <= start and span.end >= end:
                    active_styles.append(span.style)
            
            style = " ".join(active_styles) if active_styles else None
            segments.append(Segment(text, style))
        
        return segments
    
    @classmethod
    def from_markup(cls, markup: str, style: Optional[str] = None) -> "Text":
        """Create Text from Rich-style markup.
        
        Markup uses bracket syntax like [bold red]Hello[/bold red].
        
        Args:
            markup: String with markup tags.
            style: Optional base style.
            
        Returns:
            Text object with appropriate spans.
        """
        text = cls(style=style)
        
        # Pattern for markup tags
        tag_pattern = re.compile(r"\[(/)?([^\]]+)\]")
        
        style_stack: List[str] = []
        pos = 0
        last_end = 0
        
        for match in tag_pattern.finditer(markup):
            # Add text before the tag
            if match.start() > last_end:
                plain_text = markup[last_end:match.start()]
                start = len(text._text)
                text._text += plain_text
                
                # Apply current style stack
                if style_stack:
                    combined = " ".join(style_stack)
                    text._spans.append(Span(start, len(text._text), combined))
            
            is_closing = match.group(1) == "/"
            tag_content = match.group(2).strip()
            
            if is_closing:
                # Pop matching style from stack
                if style_stack and tag_content.lower() in style_stack[-1].lower():
                    style_stack.pop()
                elif style_stack:
                    # Try to remove from anywhere in stack
                    for i in range(len(style_stack) - 1, -1, -1):
                        if tag_content.lower() in style_stack[i].lower():
                            style_stack.pop(i)
                            break
            else:
                # Push new style
                style_stack.append(tag_content)
            
            last_end = match.end()
        
        # Add remaining text
        if last_end < len(markup):
            plain_text = markup[last_end:]
            start = len(text._text)
            text._text += plain_text
            
            if style_stack:
                combined = " ".join(style_stack)
                text._spans.append(Span(start, len(text._text), combined))
        
        return text
    
    @classmethod
    def assemble(cls, *parts: Union[str, Tuple[str, str], "Text"]) -> "Text":
        """Assemble Text from parts.
        
        Each part can be:
        - A string (no style)
        - A tuple of (string, style)
        - A Text object
        
        Args:
            *parts: Parts to assemble.
            
        Returns:
            Combined Text object.
        """
        result = cls()
        
        for part in parts:
            if isinstance(part, str):
                result.append(part)
            elif isinstance(part, tuple):
                text, style = part
                result.append(text, style)
            elif isinstance(part, Text):
                result.append_text(part)
        
        return result


# Alias for backward compatibility
StyledText = Text
