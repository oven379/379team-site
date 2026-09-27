import glob,re,sys
ID='113101565'
HEAD=f'''  <!-- Yandex.Metrika counter -->
  <script type="text/javascript">
    (function(m,e,t,r,i,k,a){{
      m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
      m[i].l=1*new Date();
      for (var j = 0; j < document.scripts.length; j++) {{if (document.scripts[j].src === r) {{ return; }}}}
      k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    }})(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js?id={ID}', 'ym');
    ym({ID}, 'init', {{ssr:true, webvisor:true, clickmap:true, accurateTrackBounce:true, trackLinks:true}});
  </script>
  <!-- /Yandex.Metrika counter -->
'''
BODY=f'<noscript><div><img src="https://mc.yandex.ru/watch/{ID}" style="position:absolute; left:-9999px;" alt=""/></div></noscript>\n'
def add(s):
    if 'mc.yandex.ru/metrika' in s: return s
    s=s.replace('</head>',HEAD+'</head>',1)
    s=re.sub(r'(<body[^>]*>\n)',lambda m:m.group(1)+BODY,s,count=1)
    return s
if __name__=='__main__':
    for f in ['index.html']+sorted(glob.glob('*/index.html'))+sorted(glob.glob('blog/*/index.html')):
        s=open(f).read(); n=add(s)
        if n!=s: open(f,'w').write(n); print('added',f)
