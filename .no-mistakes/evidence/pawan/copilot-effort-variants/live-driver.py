import os, subprocess as sp, pathlib as p, json, time, shlex, re, shutil, pty, fcntl, termios, struct, threading
ROOT=p.Path.cwd(); E=p.Path('/home/kumarpawa/.no-mistakes/evidence/01M3MFYGY4G18KEGCRZ56T9817'); LAB=ROOT/'.test-tmp/live'; SOCK=str(ROOT/'.ls'); LAB.mkdir()
env={'PATH':os.environ['PATH'],'HOME':str(LAB/'user'),'XDG_CONFIG_HOME':str(LAB/'xdg/config'),'XDG_CACHE_HOME':str(LAB/'xdg/cache'),'XDG_DATA_HOME':str(LAB/'xdg/data'),'XDG_STATE_HOME':str(LAB/'xdg/state'),'TMPDIR':str(LAB/'tmp'),'SHELL':'/bin/bash','TERM':'xterm-256color','OPENCODE_DISABLE_AUTOUPDATE':'1','OPENCODE_DISABLE_LSP_DOWNLOAD':'1','GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','TREEHOUSE_ROOT':str(LAB/'pool'),'FM_HOME':str(LAB/'fm'),'FM_SPAWN_NO_GUARD':'1','NO_MISTAKES_GATE':'test'}
for key in ['HOME','XDG_CONFIG_HOME','XDG_CACHE_HOME','XDG_DATA_HOME','XDG_STATE_HOME','TMPDIR']:p.Path(env[key]).mkdir(parents=True)
trans=[]; artifacts=[]; temp_paths=set()
def run(args, extra=None, cwd=ROOT, timeout=100, check=True):
 e=env.copy();e.update(extra or {});r=sp.run([str(a) for a in args],env=e,cwd=cwd,text=True,stdout=sp.PIPE,stderr=sp.STDOUT,timeout=timeout)
 trans.append({'argv':[str(a) for a in args],'rc':r.returncode,'output':r.stdout})
 if check and r.returncode:raise RuntimeError(r.stdout)
 return r
def tm(*a,**kw):return run(['tmux','-S',SOCK,*a],**kw)
try:
 run([ROOT/'bin/fm-lab-home.sh','create',env['FM_HOME']])
 home=p.Path(env['FM_HOME']);(home/'config/backlog-backend').write_text('manual\n');(home/'config/crew-harness').write_text('opencode\n');(home/'config/backend').write_text('tmux\n')
 cfg=p.Path(env['XDG_CONFIG_HOME'])/'opencode/opencode.json';cfg.parent.mkdir();cfg.write_text(json.dumps({'autoupdate':False,'provider':{'github-copilot':{'models':{}}}}))
 project=LAB/'project';run(['git','init','-q','-b','main',project]);(project/'README.md').write_text('Disposable effort validation project.\n');run(['git','-C',project,'add','README.md']);run(['git','-C',project,'-c','user.name=Lab','-c','user.email=lab@example.invalid','commit','-qm','fixture'])
 tm('-f','/dev/null','new-session','-d','-s','fm-lab-copilot','-x','120','-y','35','-c',ROOT,'bash --noprofile --norc')
 tm('set-option','-g','default-shell','/bin/bash');tm('set-option','-g','default-command','bash --noprofile --norc')
 master,slave=pty.openpty();fcntl.ioctl(slave,termios.TIOCSWINSZ,struct.pack('HHHH',35,120,0,0))
 attached=sp.Popen(['tmux','-S',SOCK,'attach-session','-t','fm-lab-copilot'],env=env,stdin=slave,stdout=slave,stderr=slave);os.close(slave)
 def drain():
  try:
   while os.read(master,65536):pass
  except OSError:pass
 threading.Thread(target=drain,daemon=True).start()
 env['TMUX']=tm('display-message','-p','-t','fm-lab-copilot','#{socket_path},#{pid},0').stdout.strip()
 catalog=run(['opencode','models','github-copilot','--verbose','--pure'],cwd='/').stdout
 (E/'live-catalog.txt').write_text(catalog)
 # Real model catalog, no credentials or synthetic model definitions.
 objs=[];decoder=json.JSONDecoder();i=0
 while True:
  j=catalog.find('\n{',i)
  if j<0:break
  o,n=decoder.raw_decode(catalog[j+1:]);objs.append(o);i=j+1+n
 variants={o['id']:list(o.get('variants',{})) for o in objs}
 assert 'xhigh' in variants['claude-opus-4.7'] and 'max' not in variants['gpt-5-mini'] and not variants['gpt-5.4-nano']
 cases=[('listed','github-copilot/claude-opus-4.7','xhigh','xhigh'),('unlisted','github-copilot/gpt-5-mini','max',None),('none','github-copilot/gpt-5.4-nano','high',None),('noeffort','github-copilot/claude-opus-4.7',None,None),('mktemp','github-copilot/claude-opus-4.7','high',None),('unavailable','github-copilot/claude-opus-4.7','high',None),('timeout','github-copilot/claude-opus-4.7','high',None),('anthropic','anthropic/claude-sonnet-4-5','high','high'),('openai','openai/gpt-5','xhigh','xhigh')]
 shim=LAB/'shim';shim.mkdir();real_mktemp=shutil.which('mktemp');mk=shim/'mktemp';mk.write_text('#!/bin/bash\ncase "$*" in "-d "*/fm-opencode-variant.XXXXXX) echo "injected variant-directory failure" >&2; exit 1;; esac\nexec '+shlex.quote(real_mktemp)+' "$@"\n');mk.chmod(0o755)
 observer=LAB/'observer';observer.mkdir();observed=observer/'opencode';calls=LAB/'catalog-calls.jsonl';real_opencode=shutil.which('opencode')
 observed.write_text('#!/usr/bin/python3\nimport os,sys,json,time,subprocess,signal\nreal='+repr(real_opencode)+'\nlog='+repr(str(calls))+'\nif sys.argv[1:2]==["models"]:\n with open(log,"a") as f:f.write(json.dumps({"argv":sys.argv[1:],"cwd":os.getcwd(),"time":time.time()})+"\\n")\n if os.environ.get("LAB_STALL_CATALOG")=="1":\n  child=subprocess.Popen([real]+sys.argv[1:])\n  time.sleep(.01)\n  os.kill(child.pid,signal.SIGSTOP)\n  with open(log,"a") as f:f.write(json.dumps({"stopped_real_opencode_pid":child.pid})+"\\n")\n  sys.exit(child.wait())\nos.execv(real,[real]+sys.argv[1:])\n');observed.chmod(0o755);env['PATH']=str(observer)+':'+env['PATH']
 for name,model,effort,expected in cases:
  task='copilot-live-'+name;run([ROOT/'bin/fm-brief.sh',task,'project','--scout'])
  brief=home/'data'/task/'brief.md';text=brief.read_text().replace('{TASK}','Read README.md and report that this disposable project exists. Make no changes.').replace('{FIRSTMATE_SPEC}','Do not access any path outside this disposable project except the supplied task records.');brief.write_text(text)
  extra={};calls.write_text('')
  if name=='mktemp':extra['PATH']=str(shim)+':'+env['PATH']
  if name=='timeout':extra.update({'LAB_STALL_CATALOG':'1','FM_OPENCODE_MODELS_TIMEOUT':'1'})
  if name=='unavailable':cfg.write_text('{"autoupdate":false}')
  args=[ROOT/'bin/fm-spawn.sh',task,project,'--scout','--harness','opencode','--backend','tmux','--model',model]
  if effort:args+=['--effort',effort]
  started=time.monotonic();r=run(args,extra,timeout=100);elapsed=time.monotonic()-started
  meta=(home/'state'/f'{task}.meta').read_text();metadata=dict(line.split('=',1) for line in meta.splitlines() if '=' in line)
  assert metadata['effort']==(effort or 'default') and metadata['model']==model
  temp_paths.add(metadata['tasktmp'])
  initial=tm('capture-pane','-p','-J','-t',metadata['window'],'-S','-500').stdout
  time.sleep(7)
  pane=tm('capture-pane','-p','-J','-t',metadata['window'],'-S','-500').stdout
  # Locate the actual generated launch command delivered to this real pane.
  match=re.search(r"\. '([^']+/launch\.[^']+\.sh)'",initial+'\n'+pane)
  if not match:
   (E/f'{name}-pane.txt').write_text(pane);raise RuntimeError('No staged launch visible for '+name)
  launchpath=p.Path(match.group(1));launch=launchpath.read_text();temp_paths.add(str(launchpath.parent))
  config=json.loads(re.search(r"OPENCODE_CONFIG_CONTENT='([^']+)'",launch).group(1))
  assert config.get('agent',{}).get('build',{}).get('variant')==expected
  assert expected is None or config['agent']['build']['model']==model
  if name in ('unlisted','none'):assert 'OpenCode lists no' in r.stdout
  if name=='none':assert 'none listed' in r.stdout
  if name in ('mktemp','unavailable'):assert 'could not read the variants' in r.stdout
  if name=='timeout':assert 'did not answer within 1s' in r.stdout and elapsed<15
  lookup_records=[json.loads(line) for line in calls.read_text().splitlines()]
  lookups=[c for c in lookup_records if 'argv' in c]
  assert len(lookups)==(0 if name in ('mktemp','noeffort','anthropic','openai') else 1)
  assert not list((LAB/'tmp').glob('fm-opencode-variant.*'))
  # The real consumer resolves precisely the emitted config; no inference/login is claimed.
  consumer=run(['opencode','debug','agent','build','--pure'],{'OPENCODE_CONFIG_CONTENT':json.dumps(config)},cwd=metadata['worktree'])
  consumer_json=json.loads(consumer.stdout)
  assert consumer_json.get('variant')==expected
  pane_pid=int(tm('display-message','-p','-t',metadata['window'],'#{pane_pid}').stdout.strip())
  processes=[];pending=[pane_pid];live_configs=[]
  while pending:
   pid=pending.pop();proc=p.Path('/proc')/str(pid)
   try:
    command=(proc/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace');values=(proc/'environ').read_bytes().split(b'\0')
    processes.append({'pid':pid,'command':command})
    for value in values:
     if value.startswith(b'OPENCODE_CONFIG_CONTENT='):live_configs.append(json.loads(value.split(b'=',1)[1]))
    children=sp.run(['pgrep','-P',str(pid)],text=True,stdout=sp.PIPE).stdout.split();pending.extend(map(int,children))
   except FileNotFoundError:pass
  assert config in live_configs, 'Emitted configuration was not present in a running worker process'
  out={'name':name,'model':model,'effort':effort,'elapsed_seconds':elapsed,'spawn_stdout':r.stdout,'metadata':metadata,'launch_command':launch,'resolved_build_agent':consumer_json,'pane':pane,'catalog_calls':lookup_records,'worker_processes':processes,'worker_configs':live_configs}
  (E/f'live-{name}.json').write_text(json.dumps(out,indent=2));artifacts.append(name)
  tm('kill-window','-t',metadata['window'])
  if name=='unavailable':cfg.write_text(json.dumps({'autoupdate':False,'provider':{'github-copilot':{'models':{}}}}))
 # Abort after the real background lookup starts, by reserving the endpoint.
 task='copilot-live-abort';run([ROOT/'bin/fm-brief.sh',task,'project','--scout'])
 brief=home/'data'/task/'brief.md';brief.write_text(brief.read_text().replace('{TASK}','Read README.md only.').replace('{FIRSTMATE_SPEC}','This spawn must refuse the duplicate endpoint.'))
 tm('new-window','-d','-t','fm-lab-copilot:','-n','fm-'+task,'-c',project)
 calls.write_text('');started=time.monotonic()
 aborted=run([ROOT/'bin/fm-spawn.sh',task,project,'--scout','--harness','opencode','--backend','tmux','--model','github-copilot/claude-opus-4.7','--effort','high'],{'LAB_STALL_CATALOG':'1','FM_OPENCODE_MODELS_TIMEOUT':'1'},check=False)
 time.sleep(4);records=[json.loads(line) for line in calls.read_text().splitlines()]
 assert aborted.returncode!=0 and 'already exists' in aborted.stdout and records
 assert not list((LAB/'tmp').glob('fm-opencode-variant.*')) and not (home/'state'/f'{task}.meta').exists()
 for record in records:
  if 'stopped_real_opencode_pid' in record:
   proc=p.Path('/proc')/str(record['stopped_real_opencode_pid'])/'stat'
   assert not proc.exists() or proc.read_text().split()[2]=='Z'
 (E/'live-abort.json').write_text(json.dumps({'stdout':aborted.stdout,'rc':aborted.returncode,'catalog_calls':records,'variant_temp_directories':[],'task_metadata_exists':False},indent=2));artifacts.append('abort')
finally:
 tm('kill-server',check=False)
 if 'attached' in globals():attached.wait(timeout=10);os.close(master)
 (E/'live-commands.json').write_text(json.dumps(trans,indent=2))
 (E/'live-completed.json').write_text(json.dumps(artifacts))
 for path in temp_paths:
  if path.startswith('/tmp/fm-copilot-live-'):shutil.rmtree(path,ignore_errors=True)
 for directory, _, _ in os.walk(LAB):os.chmod(directory,0o700)
 shutil.rmtree(LAB,ignore_errors=True)
 if p.Path(SOCK).exists():p.Path(SOCK).unlink()
