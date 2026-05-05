
import tkinter as tk
from tkinter import messagebox
import random
import string
import os


HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>

<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{image}">
<meta property="og:type" content="website">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{image}">
</head>

<body>
Redirecting...

<script>
const YT = "{url}";
const BILI = "{zh_url}";

fetch("https://ipapi.co/json/")
	.then(r => r.json())
	.then(d => {{
		if (d && d.country_code === "CN") {{
			location.href = BILI;
		}} else {{
			location.href = YT;
		}}
	}})
	.catch(() => {{
		location.href = YT;
	}});
</script>

<noscript>
<meta http-equiv="refresh" content="0;url={url}">
</noscript>

</body>
</html>
'''


def random_name(length=16):
		alphabet = string.ascii_lowercase + string.digits
		return ''.join(random.choices(alphabet, k=length))


class App:
		def __init__(self, root):
				self.root = root
				root.title('HTML Generator')

				tk.Label(root, text='Title').grid(row=0, column=0, sticky='w')
				self.title_e = tk.Entry(root, width=60)
				self.title_e.grid(row=0, column=1, padx=4, pady=4)

				tk.Label(root, text='Description').grid(row=1, column=0, sticky='w')
				self.desc_e = tk.Entry(root, width=60)
				self.desc_e.grid(row=1, column=1, padx=4, pady=4)

				tk.Label(root, text='Image URL').grid(row=2, column=0, sticky='w')
				self.img_e = tk.Entry(root, width=60)
				self.img_e.grid(row=2, column=1, padx=4, pady=4)

				tk.Label(root, text='Redirect URL').grid(row=3, column=0, sticky='w')
				self.url_e = tk.Entry(root, width=60)
				self.url_e.grid(row=3, column=1, padx=4, pady=4)

				self.use_cn = tk.IntVar()
				self.cn_cb = tk.Checkbutton(root, text='Provide Chinese (CN) URL', variable=self.use_cn, command=self._toggle_cn)
				self.cn_cb.grid(row=4, column=0, sticky='w')

				self.cn_e = tk.Entry(root, width=60)
				self.cn_e.grid(row=4, column=1, padx=4, pady=4)
				self.cn_e.configure(state='disabled')

				self.gen_btn = tk.Button(root, text='Generate HTML', command=self.generate)
				self.gen_btn.grid(row=5, column=0, columnspan=2, pady=8)

		def _toggle_cn(self):
				if self.use_cn.get():
						self.cn_e.configure(state='normal')
				else:
						self.cn_e.delete(0, tk.END)
						self.cn_e.configure(state='disabled')

		def generate(self):
				title = self.title_e.get().strip()
				desc = self.desc_e.get().strip()
				img = self.img_e.get().strip()
				url = self.url_e.get().strip()
				zh = self.cn_e.get().strip() if self.use_cn.get() else url

				if not title or not url:
						messagebox.showwarning('Missing', 'Please enter at least a title and redirect URL.')
						return

				name = random_name(16) + '.html'
				path = os.path.join(os.getcwd(), name)

				content = HTML_TEMPLATE.format(title=escape_js(title), description=escape_js(desc), image=escape_js(img or ''), url=escape_js(url), zh_url=escape_js(zh))

				try:
						with open(path, 'w', encoding='utf-8') as f:
								f.write(content)
				except Exception as e:
						messagebox.showerror('Error', f'Failed to write file: {e}')
						return

				messagebox.showinfo('Done', f'Generated: {name}\n\nPath: {path}')


def escape_js(s):
		# minimal escaping for embedding in double-quoted JS strings and HTML attributes
		return (s.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\'").replace('\n', ' '))


if __name__ == '__main__':
		root = tk.Tk()
		app = App(root)
		root.mainloop()
