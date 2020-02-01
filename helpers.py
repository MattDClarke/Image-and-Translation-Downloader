from flask import render_template

# meme generator - from CS50 finance problem set
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters. Meme writing added via url... To use special characters reserved for urls (like # or ?) you have to escape them (use different char in url to represent it)

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code
