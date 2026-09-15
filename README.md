THE ONG.PY (my organizer)

How to use the script

Save and execute
To use this organizer, copy the code and save it to a file on your computer, for example, named `organizer.py`.
You need to have Python installed on your system. Then, open your terminal (or Command Prompt), navigate to the folder where you saved the file, and type: `python organizer.py`.
It will immediately start scanning your Downloads folder and will keep running continuously, checking for new files every 2 seconds. To stop the program at any time, just press the `Ctrl` and `C` keys together in the terminal.

How the script works
The code reads your Downloads folder and ignores files that are still downloading (like `.crdownload` or `.tmp` files). As soon as the download finishes, it analyzes the file's name and its extension (like `.pdf`, `.jpg`, `.exe`). Based on that, it creates a subfolder inside Downloads and moves the file there. If a file with the same name already exists, it adds a number to the file name so it doesn't overwrite the old one.

How to customize and create your own rules
The most important part of the code for you to modify is the list called `regras` (rules). There you can change folder names, add new keywords, or add new extensions to make it easier to organize files right when you save them from your browser.

The code reads the rules from top to bottom. First, it looks for keywords in the file name. If it finds a match, it moves the file. If it doesn't, it checks the extensions.

Practical example on how to edit:
Inside the `regras` list, each block between curly braces represents a category.

If you want to create an automatic folder for your monthly bills, just add a new block to the list looking like this:

```python
{
    "pasta": "Bills to Pay",
    "descricao": "Invoices and receipts",
    "palavras_chave": ["bill", "invoice", "receipt", "statement", "nubank"],
    "extensoes": []
}

```

With the rule above added to your code, every time you download a file and save it as "internet_invoice.pdf" or "electric_bill.pdf", the script will spot the words "invoice" or "bill" and will move the file straight into the "Bills to Pay" folder, even if it is a PDF (it prioritizes the keyword over the extension).

If you want to change the name of an existing folder, just change the text in the `"pasta"` line. For example, you can change `"Imagens"` to `"Photos and Prints"`.

You can also add new extensions to the existing rules. If you start downloading `.ts` video files, just go to the `"extensoes"` line inside the "Vídeos" rule and add `".ts"` next to the others, like this: `[".mp4", ".mkv", ".avi", ".mov", ".wmv", ".webm", ".flv", ".ts"]`.

Files that do not match any keyword or extension registered in your rules will be automatically moved to a folder named "Outros" (Others). You can change the name of this default folder by modifying the variable `pasta_outros = "Outros"` in the middle of the code.
