# legges i app root hvis gunicorn skal kjøres som: gunicorn --bind 0.0.0.0:8000 wsgi:Kontroll
# som vil kjøre gunicorn modul fra nginx uten nevneverdig setup av nginx
#(endret default.conf i sites-enabled til LISTEN 8000)

# server {
#   listen 8000 jakob.kentry.no;
#   listen [::]::8000 jakob.kentry.no;
#   root /ny2/venv2;
#    # Add index.php to the list if you are using PHP
#    index.html index-blahah.html 
#  server_name _;
# }
# har ikke satt server navn under server_name og det virket. Om egentlig noe i default trengs å endres på bare for å starte serveren er jeg usikker på.

# --wsgi.py------------- 
#   

from BLOG import create_app
import pstats
import os

## OPPRETT EN CONSOLL:
def konsoll():
    a_str="logs"
    commands={"ls":os.listdir(a_str)}
    inp=input("-:")
    get_cmd=commands.get(inp)
    print (get_cmd)
    if get_cmd !=None:
        add_to=input("+:")
        prog=str(get_cmd)+add_to
        try:
            cprog=compile(source=prog,mode='exec',filename="fil.tmp")
            #cprog=compile(source=add_to,mode='exec',filename="file.tmp")
        except:
            print ("Exception!")
        finally:
            exit()
        
k=konsoll()

###

#stats = pstats.Stats('logs/GET.admin.1ms.1618581573.prof')
#stats=pstats.Stats('logs/GET.admin.6ms.1618581573.prof')
list_dir=os.listdir(path="logs")
print (list_dir)
stats=pstats.Stats('logs\POST.bruker.nybruker.134ms.1618581617.prof')
#C:\PythonVE4git\PyVE391\logs\GET.admin.1ms.1618581573.prof
stats.sort_stats('time', 'calls')
stats.print_stats()
stats.print_callers()
_=input("press enter")
# if __name__=="__main__":
#     app=create_app()
if __name__ == '__main__':
    from werkzeug.middleware.profiler import ProfilerMiddleware
    ## logger de 5 tregeste funksjonene til dir logs;
    app=create_app()
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[5], profile_dir='logs')
    app.run(debug=False)
# ----------------------wsgi.py EOF

 