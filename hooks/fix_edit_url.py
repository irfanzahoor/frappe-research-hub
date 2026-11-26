"""Fix Edit / View-source links for the i18n folder layout.

MkDocs builds page.edit_url from the file's path under docs_dir, so
with the en/ + ur/ folder layout the links come out as
.../edit/main/en/learn/... and .../edit/main/ur/learn/... — neither
path exists on main. The real files live at learn/... (English) and
i18n/ur/learn/... (Roman Urdu). Rewrite the URL per page before the
template renders it. The theme derives the View-source link from
edit_url (it swaps "edit" for "raw"), so that link is fixed too.
"""


def on_page_context(context, page, config, nav):
    edit_url = getattr(page, "edit_url", None)
    if not edit_url:
        return context
    src_uri = getattr(page.file, "src_uri", "") or ""
    if src_uri.startswith("ur/"):
        page.edit_url = edit_url.replace(
            "/edit/main/ur/", "/edit/main/i18n/ur/", 1
        )
    elif src_uri.startswith("en/"):
        page.edit_url = edit_url.replace("/edit/main/en/", "/edit/main/", 1)
    return context
