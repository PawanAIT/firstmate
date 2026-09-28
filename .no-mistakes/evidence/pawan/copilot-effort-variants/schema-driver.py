import os,subprocess as sp,pathlib as p,json,shutil
R=p.Path.cwd();L=R/'.test-tmp/schema';E=p.Path('/home/kumarpawa/.no-mistakes/evidence/01M3MFYGY4G18KEGCRZ56T9817');L.mkdir()
env={'PATH':os.environ['PATH'],'HOME':str(L/'user'),'XDG_CONFIG_HOME':str(L/'xdg/config'),'XDG_CACHE_HOME':str(L/'xdg/cache'),'XDG_DATA_HOME':str(L/'xdg/data'),'XDG_STATE_HOME':str(L/'xdg/state'),'TMPDIR':str(L/'tmp'),'FM_HOME':str(L/'fm'),'FM_BACKEND':'tmux','FM_BOOTSTRAP_DETECT_ONLY':'1','FM_BOOTSTRAP_NETWORK':'skip','FM_BOOTSTRAP_VERBOSE_FACTS':'1','TYPESAFE_API_KEY':'schema-only-no-network','GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null'}
for k in ['HOME','XDG_CONFIG_HOME','XDG_CACHE_HOME','XDG_DATA_HOME','XDG_STATE_HOME','TMPDIR']:p.Path(env[k]).mkdir(parents=True)
results=[]
def run(args):return sp.run(list(map(str,args)),env=env,text=True,stdout=sp.PIPE,stderr=sp.STDOUT,timeout=30)
try:
 assert run([R/'bin/fm-lab-home.sh','create',env['FM_HOME']]).returncode==0
 home=p.Path(env['FM_HOME']);(home/'config/backlog-backend').write_text('manual\n');brief=L/'brief.md';brief.write_text('Read a disposable project README.\n')
 cases=[('github-copilot/claude-opus-4.7',e,True) for e in ['low','medium','high','xhigh','max']]+[('anthropic/claude-sonnet-4-5','high',True),('anthropic/claude-sonnet-4-5','max',True),('openai/gpt-5','low',True),('openai/gpt-5','xhigh',True),('github-copilot/','high',False),('github-copilot/claude-opus-4.7','ultra',False),(None,'high',False),('anthropic/claude-sonnet-4-5','medium',False),('openai/gpt-5','max',False),('google/gemini-3.8-flash','high',False)]
 for model,effort,valid in cases:
  profile={'harness':'opencode','effort':effort,'provider':(model or 'github-copilot/').split('/')[0]}
  if model is not None:profile['model']=model
  (home/'config/crew-dispatch.json').write_text(json.dumps({'rules':[],'default':profile}))
  bootstrap=run([R/'bin/fm-bootstrap.sh']);resolver=run([R/'bin/fm-dispatch-resolve.sh',brief])
  results.append({'profile':profile,'expected_valid':valid,'bootstrap':{'rc':bootstrap.returncode,'output':bootstrap.stdout},'resolver':{'rc':resolver.returncode,'output':resolver.stdout}})
  if valid:
   assert 'CREW_DISPATCH: invalid' not in bootstrap.stdout and 'crew dispatch default:' in bootstrap.stdout
   assert resolver.returncode==0 and 'reason: no rules to match' in resolver.stdout
  else:
   assert 'CREW_DISPATCH: invalid' in bootstrap.stdout and resolver.returncode==2 and 'effort must be supported by its harness and model' in resolver.stdout
finally:
 (E/'live-profile-validation.json').write_text(json.dumps(results,indent=2));shutil.rmtree(L)
