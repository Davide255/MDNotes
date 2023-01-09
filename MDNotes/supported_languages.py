from pygments import lexers as _lex

Lexer = _lex.find_lexer_class_by_name

all_lexers = {
    "c": [Lexer("c"), "language-c", False],
    "cpp": [Lexer("cpp"), "language-cpp", False],
    "csharp": [Lexer("csharp"), "language-csharp", False],
    "css": [Lexer("css"), "language-css3", False],
    "fortran": [Lexer("fortran"), "language-fortran", False],
    "go": [Lexer("go"), "language-go", False],
    "haskell": [Lexer("haskell"), "language-haskell", False],
    "html": [Lexer("html"), "language-html5", True],
    "reStructuredText": [Lexer("reStructuredText"), "", True],
    "java": [Lexer("java"), "language-java", False],
    "javascript": [Lexer("javascript"), "language-javascript", False],
    "kotlin": [Lexer("kotlin"), "language-kotlin", False],
    "lua": [Lexer("lua"), "language-lua", False],
    "markdown": [Lexer("markdown"), "language-markdown", True],
    "php": [Lexer("php"), "language-php", False],
    "python": [Lexer("python"), "language-python", False],
    "r": [Lexer("r"), "language-r", False],
    "ruby": [Lexer("ruby"), "language-ruby", False],
    "rust": [Lexer("rust"), "language-rust", False],
    "swift": [Lexer("swift"), "language-swift", False],
    "typescript": [Lexer("typescript"), "language-typescript", False],
}

'''from kivymd import icon_definitions

txt = []

for i in icon_definitions.md_icons:
    if i.startswith('language'):
        name = i.replace('language-', '')
        txt.append('"{}": [Lexer("{}"), "%s", False],'.replace('{}', name if name.isalpha() else ''.join(list(name)[:-1])).replace('%s', 'language-'+name))

print('\n    '.join(txt))'''