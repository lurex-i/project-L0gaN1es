class Note:
    def __init__(self, text: str, tags: set | None = None):
        self.text = text
        self.tags = tags if tags else set()

    def edit_text(self, new_text: str):
        self.text = new_text

    def add_tag(self, tag: str):
        self.tags.add(tag.lower())

    def remove_tag(self, tag: str):
        self.tags.discard(tag.lower())

    def __str__(self):
        tags_str = ", ".join(self.tags) if self.tags else "no tags"
        return f"Note: {self.text} | Tags: {tags_str}"