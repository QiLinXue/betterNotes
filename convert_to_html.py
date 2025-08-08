import re
import sys
import markdown2
import json

def heading_label(content):

    lines = content.splitlines()
    label = 0

    for i, line in enumerate(lines):
        if re.match(r'^##\s', line):
            label += 1
            lines[i] = f'# {label} {line[3:]}'
        elif re.match(r'^###\s', line):
            lines[i] = f'## {label} {line[4:]}'

    return '\n'.join(lines)

def convert_to_html(md_content):
    head = '''
        <!-- <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" integrity="sha512-dTfge/zgoMYpP7QbHy4gWMEGsbsdZeCXz7irItjcC3sPUFtf0kuFbDz/ixG7ArTxmDjLXDmezHubeNikyKGVyQ==" crossorigin="anonymous"> -->

        <!-- Bootstrap Style -->
        <link
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css"
          rel="stylesheet"
          integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor"
          crossorigin="anonymous"
        />

        <!-- TOC CSS -->
        <link rel="stylesheet" href="https://afeld.github.io/bootstrap-toc/bootstrap-toc.css">

        <link rel="stylesheet" href="https://afeld.github.io/bootstrap-toc/assets/screen.css" media="screen" charset="utf-8">

        <script
          src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
          integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
          crossorigin="anonymous"
        ></script>

        <script
        src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2"
        crossorigin="anonymous"
      ></script>
      <script src="https://afeld.github.io/bootstrap-toc/bootstrap-toc.js"></script>
          
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <link rel="stylesheet"
          href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/default.min.css">
    <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
    <link rel="stylesheet" type="text/css" href="https://tikzjax.com/v1/fonts.css">
    <script src="https://tikzjax.com/v1/tikzjax.js"></script>
    '''

    '''
    ----------------- First, we do the custom markdown to HTML styles -------------------
    '''

    # Title
    # Replace space with dash
    md_content = re.sub(
        r'# (.+)', 
        r'<h1 id="-Title">\1</h1>',
        md_content,
        1)
    
    # HTML Title but only if it exists
    search_res = re.search(r'<h1 id="-(.+)">(.*?)</h1>', md_content)
    if search_res: 
      title = search_res.group(2) 
    else:
      title = 'Untitled'

    # Headings
    md_content = heading_label(md_content)


    '''
    --------------------- Use Markdown2 to do the dirty work ------------------------
    '''
    
    md_content = markdown2.markdown(md_content, extras=['fenced-code-blocks', 'cuddled-lists', 'header-ids', 'code-friendly'])
    '''
    ------------------ Now we can customize the HTML further ------------------
    '''
    # Format headings better
    md_content = re.sub(r'<h1 id="(.*?)-(.*?)">(\d+)', r'<h1 id="L\1">', md_content)
    md_content = re.sub(r'<h2 id="(.*?)-(.*?)">(\d+)', r'<h2 id="L\1-\2">', md_content)

    # block equations
    md_content = re.sub(r'\$\$([^\$]+)\$\$', r'\[ \1 \]', md_content)
    
    # in-line equations
    md_content = re.sub(r'\$([^\$]+)\$', r'\( \1 \)', md_content)

    # images (add width="100%")
    md_content = re.sub(r'<img src="(.+?)" alt="(.*?)" />', r'<img src="\1" alt="\2" width="100%" />', md_content)

    # \verb## environment (turns <code>@text@</code> into \(\verb#text#\) )
    md_content = re.sub(r'<code>@(.+)@</code>', r'\(\\verb#\1#\)', md_content)

    # Tikzpicture
    md_content = re.sub(
          r'<pre><code>tikz((.|\n)*?)</code></pre>',
          r'<center><script type="text/tikz">\\begin{tikzpicture}[scale=2]\1\\end{tikzpicture}</script></center>',
          md_content
      )
    
    # Change -&gt; to -> but only if surrounded by \begin{tikzpicture} and \end{tikzpicture}
    md_content = re.sub(
          r'\\begin{tikzpicture}((.|\n)*?)\\end{tikzpicture}',
          lambda x: x.group(0).replace('-&gt;', '->'),
          md_content
      )
    
    # Plot (convert <code>@plot domain:-10:10 x^2+2*x+1</code> into tikzpicture)
    # NOTE: NOT WORKING
    md_content = re.sub(
          r'<pre><code>plot\ndomain=(.*?):(.*?)\n(.*?)\n</code></pre>',
          lambda x: f'<center><script type="text/tikz">\\begin{{tikzpicture}}[scale=2]\\begin{{axis}}[legend pos=outer north east,axis lines = box,xlabel = $x$,ylabel = $y$,variable = t,trig format plots = rad,]\\addplot [domain={x.group(1)}:{x.group(2)},samples=70,color=blue,]{{{x.group(3)}}};\\end{{axis}}\\end{{tikzpicture}}</script></center>',
          md_content
      )
    
    # Definitions
    md_content = re.sub(
        r'@@DEF\n((.|\n)*?)@@',
        r'<div class="alert alert-success" role="alert">\1</div>',
        md_content
    )
    
    # Theorems
    md_content = re.sub(
        r'@@THM\n((.|\n)*?)@@',
        r'<div class="alert alert-primary" role="alert">\1</div>',
        md_content
    )

    # Proofs
    md_content = re.sub(
        r'@@PRF\n((.|\n)*?)@@',
        r'<div class="alert alert-dark" role="alert">\1</div>',
        md_content
    )

    '''
    ------------------ Finally, we can put it all together ------------------
    '''
    html_template = f'''<!DOCTYPE html>
<html>
  <head>
  <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
  {head}
  </head>
<body data-bs-spy="scroll" data-target="#toc">
  <div class="container">
    <div class="row">
      <div class="col-sm-3">
        <nav id="toc" data-toggle="toc" class="sticky-top"></nav>
      </div>      <div class="col-sm-9">
          {md_content}
        </div>
      </div>
    </div>
  </body>
</html>
'''
    return html_template

def main(input_file, output_file):
    input_filename = input_file
    output_filename = output_file

    with open(input_filename, 'r') as f:
        md_content = f.read()

    html_content = convert_to_html(md_content)

    with open(output_filename, 'w') as f:
        f.write(html_content)

if __name__ == '__main__':
    # Read input from stdin
    input_md = sys.stdin.read()
    output_html = convert_to_html(input_md)
    print(json.dumps({"html_content": output_html}))
