import runpy, sys, json, pathlib, shlex
sys.argv=['live-spawn-driver.py']
s=runpy.run_path('/home/kumarpawa/.no-mistakes/evidence/01M3MDRF9H7N4F6XWPBX8M7NFW/live-spawn-driver.py')
L=s['L']; E=s['E']; git=s['git']; run=s['run']; tmux=s['tmux']
p=L/'missing/project'; origin=L/'missing/origin.git'; old=json.loads((E/'live-missing.json').read_text())
marker=pathlib.Path(git(p,'rev-parse','--path-format=absolute','--git-path','common/fm-origin-head-refreshed')); stamp=marker.read_text()
print(run(['treehouse','lease','1','--lease-holder','live-shared-proof'],cwd=p).stdout)
git(origin,'symbolic-ref','HEAD','refs/heads/main')
contacts=L/'missing/contacts.jsonl'; contacts.write_text('')
task='live-shared'; brief=L/'home/data'/task/'brief.md'; brief.parent.mkdir(); brief.write_text('# Task\n## Captain\'s intent\nObserve the current Git commit without modifying files or running remote commands or pipelines.\n\n## Firstmate spec\nRemain idle in this disposable validation.\n')
cmd=['bin/fm-spawn.sh',task,str(p),'--mode','direct-PR','--yolo','off','--harness','opencode','--backend','tmux']
print('$ '+shlex.join(cmd)); result=run(cmd); print(result.stdout)
fields=dict(line.split('=',1) for line in (L/'home/state'/f'{task}.meta').read_text().splitlines() if '=' in line); wt=fields['worktree']
marker2=git(wt,'rev-parse','--path-format=absolute','--git-path','common/fm-origin-head-refreshed')
c=[json.loads(x) for x in contacts.read_text().splitlines()]
obs={'first_slot':old['worktree'],'second_slot':wt,'first_marker':str(marker),'second_marker':marker2,'marker_before':stamp.strip(),'marker_after':marker.read_text().strip(),'origin_head':git(p,'symbolic-ref','refs/remotes/origin/HEAD'),'head':git(wt,'rev-parse','HEAD'),'contacts':c,'metadata':fields}
print(json.dumps(obs,indent=2)); (E/'live-shared.json').write_text(json.dumps(obs,indent=2)+'\n')
assert wt!=old['worktree']; assert marker2==str(marker); assert marker.read_text()==stamp
assert obs['origin_head']=='refs/remotes/origin/trunk'; assert obs['head']==old['expected']
assert len([x for x in c if x['cwd']==wt])==1
assert git(p,'rev-parse','HEAD')==old['initial']
print('SCENARIO PASS shared clone marker across distinct real Treehouse slots (direct-PR ship)')
tmux('kill-window','-t',fields['window'])
