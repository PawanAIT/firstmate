#!/usr/bin/env python3
"""Disposable real fm-spawn + tmux + Treehouse proof; no mocked executables."""
import os, pathlib, subprocess, json, time, sys, shlex
R=pathlib.Path.cwd(); L=R/'.l'; E=pathlib.Path('/home/kumarpawa/.no-mistakes/evidence/01M3MDRF9H7N4F6XWPBX8M7NFW')
env=os.environ.copy()
for k in ['NO_MISTAKES_GATE','FM_GATE_REFUSE_BYPASS','FM_ROOT_OVERRIDE','FM_STATE_OVERRIDE','FM_DATA_OVERRIDE','FM_CONFIG_OVERRIDE','FM_PROJECTS_OVERRIDE','FM_TASK_ID','TASKS_AXI_FILE','TASKS_AXI_BACKEND']:
    env.pop(k,None)
env.update(HOME=str(L/'user'), XDG_CONFIG_HOME=str(L/'user/config'), XDG_DATA_HOME=str(L/'user/data'), XDG_CACHE_HOME=str(L/'user/cache'), FM_HOME=str(L/'home'), TMUX_TMPDIR=str(L/'tmux'), TREEHOUSE_ROOT=str(L/'trees'), GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1', GIT_AUTHOR_NAME='Spawn lab', GIT_AUTHOR_EMAIL='lab@example.invalid', GIT_COMMITTER_NAME='Spawn lab', GIT_COMMITTER_EMAIL='lab@example.invalid', FM_SPAWN_NO_GUARD='1', FM_ORIGIN_HEAD_REFRESH_SECONDS='600', SHELL='/bin/bash')
def run(args, cwd=None, check=True, extra=None):
    p=subprocess.run([str(x) for x in args],cwd=cwd or R,env=env| (extra or {}),text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=100)
    if check and p.returncode: raise RuntimeError(f'{args}: {p.stdout}')
    return p

def git(cwd,*args,check=True): return run(['git','-C',cwd,*args],check=check).stdout.strip()
def tmux(*args): return run(['tmux','-L','fm-lab',*args]).stdout.strip()
env['TMUX']=tmux('display-message','-p','-t','primary','#{socket_path},#{pid},0')
for k in ['HOME','XDG_CONFIG_HOME','XDG_DATA_HOME','XDG_CACHE_HOME','TREEHOUSE_ROOT','GIT_CONFIG_GLOBAL','GIT_CONFIG_NOSYSTEM','SHELL']:
    tmux('set-environment','-g',k,env[k])
tmux('set-option','-g','default-shell','/bin/bash')
tmux('set-option','-g','default-command','/bin/bash --noprofile --norc')

def scenario(name):
    d=L/name; d.mkdir(); p=d/'project'; o=d/'origin.git'; pub=d/'publisher'
    git(d,'init','-q','-b','main',str(p))
    (p/'base.txt').write_text('base\n'); git(p,'add','.'); git(p,'commit','-qm','base')
    initial=git(p,'rev-parse','HEAD')
    git(d,'clone','-q','--bare',str(p),str(o)); git(p,'remote','add','origin','file://'+str(o))
    git(p,'fetch','-q','origin'); git(p,'remote','set-head','origin','--auto')
    git(d,'clone','-q','file://'+str(o),str(pub))
    (pub/'advanced.txt').write_text('published after allocation\n'); git(pub,'add','.'); git(pub,'commit','-qm','advanced'); git(pub,'push','-q','origin','main')
    current=git(pub,'rev-parse','HEAD')
    marker=pathlib.Path(git(p,'rev-parse','--path-format=absolute','--git-path','common/fm-origin-head-refreshed')); marker.parent.mkdir(exist_ok=True)
    stamp=str(int(time.time())-60); marker.write_text(stamp+'\n')
    window='600'
    if name in ['missing','failure-missing']: marker.unlink()
    if name in ['expired','failure-expired']: marker.write_text(str(int(time.time())-3600)+'\n')
    if name=='future': marker.write_text(str(int(time.time())+3600)+'\n')
    if name=='invalid': marker.write_text('not-a-time\n')
    if name=='unwritable': marker.unlink(); marker.mkdir()
    if name=='disabled': window='0'
    if name=='empty-window': window=''
    if name=='invalid-window': window='bad'
    if name=='custom-window': window='30'
    if name not in ['advanced','late-advance','unreachable','unreachable-after-allocation'] and not name.startswith('failure'):
        git(pub,'push','-q','origin','HEAD:refs/heads/trunk'); git(o,'symbolic-ref','HEAD','refs/heads/trunk')
    if name in ['switched','renamed']:
        git(pub,'checkout','-qb','trunk'); (pub/'trunk-only.txt').write_text('new default\n'); git(pub,'add','.'); git(pub,'commit','-qm','new-default'); git(pub,'push','-q','origin','trunk'); current=git(pub,'rev-parse','HEAD')
        if name=='renamed': git(o,'update-ref','-d','refs/heads/main')
    if name.startswith('failure'): git(o,'symbolic-ref','HEAD','refs/heads/no-such-default')
    if name=='unreachable': git(p,'remote','set-url','origin','file://'+str(d/'absent.git'))
    contacts=d/'contacts.jsonl'; contacts.write_text('')
    wrapper=d/'upload-pack'
    wrapper.write_text('#!/usr/bin/env python3\nimport os,json\nwith open('+repr(str(contacts))+',"a") as f: f.write(json.dumps({"cwd":os.getcwd(),"ppid":os.getppid()})+"\\n")\nos.execvp("git",["git","upload-pack"]+__import__("sys").argv[1:])\n'); wrapper.chmod(0o755)
    if name=='unreachable-after-allocation':
        wrapper.write_text(wrapper.read_text().replace('os.execvp("git",', 'if os.getcwd() != '+repr(str(p))+': __import__("sys").argv[1:] = ['+repr(str(d/'absent.git'))+']\nos.execvp("git",'))
    if name=='late-advance':
        (pub/'late.txt').write_text('published after Treehouse allocation\n'); git(pub,'add','.'); git(pub,'commit','-qm','late-publish'); current=git(pub,'rev-parse','HEAD')
        insertion='if os.getcwd() != '+repr(str(p))+':\n import subprocess\n before=subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()\n with open('+repr(str(d/'head-before-refresh'))+',"w") as f: f.write(before)\n subprocess.run(["git","-C",'+repr(str(pub))+',"push","--quiet","origin","main"],check=True)\n'
        wrapper.write_text(wrapper.read_text().replace('os.execvp("git",', insertion+'os.execvp("git",'))
    git(p,'config','remote.origin.uploadpack',str(wrapper))
    task='live-'+name; brief=L/'home/data'/task/'brief.md'; brief.parent.mkdir(parents=True)
    brief.write_text("# Task\n## Captain's intent\nObserve the current Git commit without changing files. Do not run any pipeline or remote commands.\n\n## Firstmate spec\nThis disposable launch validates the spawn base. Remain idle.\n")
    old=marker.read_text().strip() if marker.is_file() else ('directory' if marker.is_dir() else None)
    before=int(time.time()); cmd=['bin/fm-spawn.sh',task,str(p),'--scout','--harness','opencode','--backend','tmux']
    out=run(cmd,check=False,extra={'FM_ORIGIN_HEAD_REFRESH_SECONDS':window}); after=int(time.time())
    print('$ FM_ORIGIN_HEAD_REFRESH_SECONDS='+repr(window)+' '+shlex.join(cmd),flush=True); print(out.stdout,flush=True)
    meta=L/'home/state'/f'{task}.meta'; fields=dict(line.split('=',1) for line in meta.read_text().splitlines() if '=' in line) if meta.exists() else {}
    wt=fields.get('worktree')
    if not wt:
        trees=git(p,'worktree','list','--porcelain').splitlines(); paths=[x[9:] for x in trees if x.startswith('worktree ') and x[9:]!=str(p)]; wt=paths[0] if paths else None
    c=[json.loads(x) for x in contacts.read_text().splitlines()]
    new=marker.read_text().strip() if marker.is_file() else ('directory' if marker.is_dir() else None)
    observation={'scenario':name,'exit':out.returncode,'initial':initial,'expected':current,'worktree':wt,'head':git(wt,'rev-parse','HEAD') if wt else None,'origin_head':git(p,'symbolic-ref','refs/remotes/origin/HEAD'),'marker_before':old,'marker_after':new,'before':before,'after':after,'contacts':c,'metadata':fields,'refs':git(wt,'for-each-ref','--format=%(refname)') if wt else ''}
    print(json.dumps(observation,indent=2),flush=True)
    (E/f'live-{name}.json').write_text(json.dumps(observation,indent=2)+'\n')
    if out.returncode==0:
        assert observation['head']==current, 'wrong base'
        expected_branch='main' if name in ['advanced','late-advance','fresh','empty-window','invalid-window'] else 'trunk'
        assert observation['origin_head']=='refs/remotes/origin/'+expected_branch, 'wrong default branch'
        assert 'refs/worktree/fm-spawn-origin-head' not in observation['refs'], 'leaked probe'
        fast=name in ['advanced','late-advance','fresh','empty-window','invalid-window']
        if fast: assert new==old, 'fast path extended window'
        elif name!='unwritable': assert before<=int(new)<=after, 'missing current timestamp'
        print('POOLED_CONTACTS', [x for x in c if x['cwd']==wt],flush=True)
        assert len([x for x in c if x['cwd']==wt])==(1 if fast else (4 if name in ['switched','renamed'] else 3)), 'unexpected freshness contacts'
        tmux('capture-pane','-p','-t',fields['window'])
        tmux('kill-window','-t',fields['window'])
    else:
        assert name.startswith('failure') or name.startswith('unreachable'),'unexpected spawn refusal'
        assert not fields and new==old, 'refusal published metadata or refreshed marker'
        assert 'refusing to launch from a potentially stale base' in out.stdout, 'wrong refusal'
    if name=='late-advance':
        pool_before=(d/'head-before-refresh').read_text(); assert pool_before!=current, 'fixture did not stale the allocated worktree'
        print('Allocated HEAD before freshness:',pool_before,'; HEAD after:',observation['head'],flush=True)
    print('SCENARIO PASS',name,flush=True)

for name in sys.argv[1:]: scenario(name)
