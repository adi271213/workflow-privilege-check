import html


def _text(value):
    text = html.escape(str(value)).replace("\n", " ").replace("\r", " ")
    # Keep repository-controlled names literal, including Markdown links/images,
    # emphasis and backslashes that could alter the surrounding table.
    return "".join(f"&#{ord(char)};" if char in "\\`*_[]()!|~" else char for char in text)


def markdown(report: dict) -> str:
    status = report["analysis"]
    if status != "complete":
        title = "Analysis " + status
    elif report["findings"]:
        title = "Review suggested"
    else:
        title = "No supported privilege expansions detected"
    lines = [f"## {title}", "", f"Base: `{_text(report['base'])}`", f"Head: `{_text(report['head'])}`", ""]
    if report["findings"]:
        lines += ["| Rule | Workflow | Job | Change |", "|---|---|---|---|"]
        for item in report["findings"]:
            lines.append("| " + " | ".join(_text(item[key] or "—") for key in ("rule", "file", "job", "message")) + " |")
        lines.append("")
    for item in report["diagnostics"]:
        lines.append(f"- {_text(item['side'])}: {_text(item['file'])}, job {_text(item['job'] or '—')}: {_text(item['reason'])}")
    for assumption in report.get("assumptions", []):
        lines += ["", "Assumption: " + _text(assumption)]
    lines += ["", "Scope: configured capability changes only. This report does not establish PR safety."]
    return "\n".join(lines) + "\n"
