# Troubleshooting — Error Library

Woh page jo aap kholte hain jab kuch toot jaye. Har entry aik asal
error hai jo beginner ya intermediate developer ko waqai hota hai —
exact message, kyun hota hai, aur fix — order mein. Koi theory nahi,
sirf steps.

## Kuch theek karne se pehle — pehle 3 checks

Zyada tar errors in mein se aik se hal ho jate hain, code chhune se
pehle:

1. **Error ki AAKHRI lines parhein, pehli nahi.** Traceback aik
   stack hota hai: pehli lines batati hain ke code kahan se call hua,
   aakhri line khud exception hoti hai — `OperationalError`,
   `LinkValidationError`, `ModuleNotFoundError`. Woh aakhri line hi
   aap ki problem ka naam hai. Usay search karein, poora trace nahi.
2. **Desk mein Error Log check karein.** Awesome bar mein "Error Log"
   search karein — har server error wahan full traceback ke saath
   save hota hai, woh bhi jo screen par sirf "Something went wrong"
   dikhata hai. Agar aik hi error baar baar aa raha hai, to sab se
   nayi entry parhein.
3. **`bench doctor` chalaye.** Bench directory se aik command, jo
   scheduler, background workers, Redis aur Socket.IO ka status
   dikhata hai. Agar in mein se koi band hai, to is guide ke aadhe
   errors usi aik wajah se hain.

Agar aap upgrade ke beech mein hain, to pehle backup lein:
`bench --site <site> backup` — aik fix jo undo ho sake, woh fix
aap try kar sakte hain.

---

## Stage A — Setup aur Install

### A1 — v16 ke liye ghalat Python / Node / MariaDB version

```text
ERROR: This version of Frappe requires Python 3.14 or newer
```

ya install aadha hota hai aur version ki shikayat par ruk jata hai.

**Kab hota hai:** naye server par `bench init` karte waqt, ya purane
bench par v16 upgrade karte waqt.

**Kyun hota hai:** v16 ne apni minimum requirements barha di hain:
**Python 3.14, Node 24, MariaDB 11.8, Redis/Valkey 6+, Yarn 1.22+**.
Purana bench Python 3.10 / Node 18 par bana tha, aur v16 ka code us
par import hi nahi hota.

**Fix:**

1. Check karein ke aap ke paas asal mein kya hai:
   ```bash
   python3 --version && node -v && mariadb --version
   ```
2. Sahi Python install karein aur usi se bench banayein:
   ```bash
   bench init --frappe-branch version-16 --python python3.14 frappe-bench
   ```
3. Agar bench pehle se ghalat Python par bana hai, to use wahin
   patch karne ki koshish na karein — virtualenv dobara Python 3.14
   par banayein (dekhein
   [Upgrade guide](upgrade-v14-v15-v16.md)).

**Prevention:** kisi bhi install ya upgrade se pehle
[Upgrade guide](upgrade-v14-v15-v16.md) ka version matrix parhein
aur paanchon versions match karein — Python, Node, MariaDB, Redis,
Yarn — sirf aik nahi.

### A2 — MariaDB access denied for root

```text
pymysql.err.OperationalError: (1045, "Access denied for user 'root'@'localhost' (using password: YES)")
```

**Kab hota hai:** fresh install par `bench new-site` ya
`bench migrate` karte waqt.

**Kyun hota hai:** bench MariaDB mein us password se login karta hai
jo site ki config mein save hai, aur woh MariaDB ke asal `root`
password se match nahi karta. Aam tor par MariaDB ka root password
install ke waqt set hua tha aur bench ko kabhi bataya nahi gaya — ya
baad mein badal diya gaya.

**Fix:**

1. Check karein ke bench kya password samajhta hai:
   ```bash
   cat sites/<site>/site_config.json | grep db_password
   ```
2. MariaDB mein root se login karein aur password match kar dein:
   ```bash
   sudo mysql -u root
   ```
   ```sql
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'the-password-from-site_config.json';
   FLUSH PRIVILEGES;
   ```
3. Test karein:
   ```bash
   bench --site <site> migrate
   ```

**Prevention:** MariaDB ka root password install ke waqt likh lein
aur us server ki har site ke liye wohi use karein. Aik server, aik
password — har site ka alag password nahi.

### A3 — MariaDB chal hi nahi rahi

```text
pymysql.err.OperationalError: (2002, "Can't connect to local MySQL server through socket '/run/mysqld/mysqld.sock'")
```

**Kab hota hai:** server reboot ke baad koi bhi bench command, ya
fresh install par jahan MariaDB kabhi start hi nahi hui.

**Kyun hota hai:** MariaDB aik alag service hai. Agar woh band hai,
to Frappe database tak nahi pahunch sakta — error socket file ke
baare mein hai, aap ki site ke baare mein nahi.

**Fix:**

```bash
sudo systemctl status mariadb
sudo systemctl start mariadb
sudo systemctl enable mariadb   # har boot par start ho, sirf ab nahi
bench --site <site> migrate     # confirm karein ke site dobara connect ho gayi
```

**Prevention:** install ke waqt service ko `enable` karein (upar
step 3), sirf `start` nahi. Har reboot ke baad `bench doctor` aik
command mein check kar deta hai.

### A4 — Redis connection refused

```text
redis.exceptions.ConnectionError: Error 111 connecting to 127.0.0.1:13000. Connection refused.
```

**Kab hota hai:** `bench start` karte waqt, ya site load hoti hai
lekin background jobs aur caching chup chaap kuch nahi karte.

**Kyun hota hai:** Frappe queue, cache aur Socket.IO ke liye Redis
se baat karta hai. Agar Redis band hai, to web process start ho jata
hai lekin queue wali koi cheez kaam nahi karti — aur error mein port
likha hota hai (dev bench par 11000, 12000 ya 13000, production mein
6379).

**Fix:**

```bash
redis-cli ping        # jawab PONG hona chahiye
sudo systemctl status redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
bench doctor          # confirm karein ke teeno queues ke liye Redis wapas aa gaya
```

**Prevention:** MariaDB ki tarah — install ke waqt service enable
karein. v16 mein Redis ki jagah Valkey bhi chal sakta hai; dono mein
se aik ko `bench start` se pehle chalna hi chahiye.

### A5 — `bench build` assets / Yarn par fail ho jata hai

```text
error Command failed.
Exit code: 1
Command: /usr/bin/node .../yarn install
```

**Kab hota hai:** `bench update` ke baad, app install karne ke baad,
ya fresh bench par.

**Kyun hota hai:** JavaScript build ko sahi Node version chahiye
(v16 ko Node 24) aur kaam karta Yarn install. Do aam wajahen hain:
ghalat Node version (dekhein A1) aur aadha install ya kharab
`node_modules`.

**Fix:**

1. Pehle Node check karein: `node -v` — v16 ko v24 chahiye.
2. Bench ki dependencies dobara install karein, phir build karein:
   ```bash
   bench setup requirements
   bench build
   ```
3. Agar aik app masla kar rahi hai, to sirf use build karein:
   ```bash
   bench build --app <app>
   ```
   aur failure se just upar wali lines parhein — woh batati hain ke
   kis file ne build toda.

**Prevention:** `apt` se doosra Node version pehle wale ke upar
install karke bhool na jayein ke PATH par kaun sa hai. Poore server
ke liye aik Node manager use karein aur version apne install notes
mein likh lein.

### A6 — `ModuleNotFoundError: No module named 'frappe'`

```text
ModuleNotFoundError: No module named 'frappe'
```

**Kab hota hai:** koi bhi `bench` command, ya Python script jo frappe
import karta hai.

**Kyun hota hai:** aap command ghalat directory se chala rahe hain,
ya us shell mein bench ka virtualenv path par nahi hai. `frappe`
sirf bench ke `env/` ke andar mojood hota hai.

**Fix:**

1. Bench directory mein jayein aur dobara try karein:
   ```bash
   cd ~/frappe-bench
   bench --version
   ```
2. Agar phir bhi fail ho, to virtualenv kharab hai — bench ki
   requirements dobara install karein:
   ```bash
   bench setup requirements
   ```

**Prevention:** bench commands chalane se pehle hamesha bench
directory mein `cd` karein. Bench ka path apne shell notes mein
likhein, yaad mein nahi.

### A7 — Port 8000 pehle se use mein hai

```text
OSError: [Errno 98] Address already in use
```

**Kab hota hai:** `bench start` karte waqt jab doosra bench (ya
purana, abhi bhi chalta hua) pehle se port 8000 par hai.

**Kyun hota hai:** aik port par sirf aik process sun sakta hai. Aam
wajah yeh hai ke `bench start` kabhi theek se band nahi hua — us ka
terminal band kar diya gaya lekin processes chalte rahe.

**Fix:**

1. Pata lagayein ke port kis ke paas hai:
   ```bash
   sudo lsof -i :8000
   ```
2. Purane bench ko theek se band karein (us ki directory se
   `bench stop`), ya process ko us ke PID se band karein:
   ```bash
   kill <pid>
   ```
3. Ya is bench ko doosra port dein — `sites/common_site_config.json`
   mein add karein:
   ```json
   "webserver_port": 8001
   ```
   phir bench restart karein.

**Prevention:** aik bench, aik port — likh kar rakhein. Dev bench ko
us ke apne terminal mein Ctrl+C se band karein, terminal window band
karke nahi.

---

## Stage B — Development

### B1 — `bench migrate` patch par fail ho jata hai

```text
frappe.modules.patch_handler.PatchError: Patch myapp.patches.v16_0.fix_data execute failed
```

ya:

```text
ModuleNotFoundError: No module named 'frappe.patches.v15_0.some_patch'
Migration exit code: 1
```

**Kab hota hai:** update ke baad ya naya app code pull karne ke baad
`bench migrate` karte waqt.

**Kyun hota hai:** patch aik one-off script hota hai jo app ki
`patches.txt` mein likha hota hai. Woh fail hota hai kyun ke us ki
file missing hai (adhoora update), us ke code mein bug hai, ya woh
aisa data expect karta hai jo mojood nahi. Migrate pehle fail hone
wale patch par ruk jata hai — us ke baad wali koi cheez abhi chali hi
nahi.

**Fix:**

1. Error se fail hone wale patch ka naam parhein — wohi pehli cheez
   hai jo theek karni hai, poora migrate nahi.
2. Check karein ke apps matching branches par hain:
   ```bash
   bench version --format table
   git -C apps/frappe status --short
   git -C apps/frappe branch --show-current
   ```
   Disk se patch file missing hai, to matlab update poora nahi hua —
   matching release se sahi app code wapas layein, phir
   `bench --site <site> migrate` dobara chalaye.
3. Agar patch ka code khud kharab hai, to us ka code theek karein,
   phir `patches.txt` mein us ki line par date comment laga kar use
   dobara chalaye:
   ```text
   myapp.patches.v16_0.fix_data #2026-11-26
   ```
   phir `bench --site <site> migrate` dobara chalaye.
4. Sirf aakhri hal: `bench --site <site> migrate --skip-failing`
   patch ko skip karke done mark kar deta hai. Sirf tab use karein
   jab aap ko yaqeen ho ke patch skip karna safe hai — skip ki hui
   data patch woh data purani shape mein chhod deti hai, aur site
   theek lagti hai jab tak woh theek nahi rehti.

**Prevention:** har migrate se pehle backup lein
(`bench --site <site> backup`), aur migration pehle staging par
chalaye. Production par `migrate` pehli dafa kabhi bhi na chalaye.

### B2 — Code change ke baad `Unknown column`

```text
pymysql.err.OperationalError: (1054, "Unknown column 'tabSales Order.new_field' in 'field list'")
```

**Kab hota hai:** DocType mein field add karne ke baad, ya app ki
branch switch karne ke baad.

**Kyun hota hai:** code ko field ka pata hai lekin database ko nahi —
`migrate` mein schema sync chala hi nahi, ya us code par chala jo ab
install nahi hai.

**Fix:**

```bash
bench --site <site> migrate
bench --site <site> clear-cache
```

Agar phir bhi fail ho, to code aur branch mein farq hai —
`git -C apps/<app> status` se uncommitted ya aadhi pull hui changes
check karein, branch theek karein, aur dobara migrate karein.

**Prevention:** har DocType change `migrate` par khatam hoti hai,
har dafa, test karne se pehle. Dekhein
[Lesson 03](../learn/framework/level-1/03-first-doctype.md).

### B3 — DocType kholte waqt "Not Permitted"

```text
Not Permitted
You do not have enough permissions to access this document.
```

**Kab hota hai:** user aik DocType ya document kholta hai jo
Administrator aaram se khol leta hai.

**Kyun hota hai:** user ke role ko us DocType par permission nahi,
ya User Permission use sirf kuch documents tak restrict karta hai
(misal, sirf apni company ke records).

**Fix:**

1. **Role Permission Manager** kholein, DocType chunein, aur user ke
   role wali row check karein — read, write, create, submit, delete
   alag alag ticks hain. Jo kaam chahiye, woh tick karein, us se
   zyada nahi.
2. Us user ki **User Permissions** check karein — aik Company ya
   Warehouse ki restriction baqi sab kuch chhupa deti hai.
3. Asal user ke tor par test karein, Administrator ke tor par nahi
   — Administrator sab kuch dekhta hai, is liye Administrator ke tor
   par test karna kuch test karna nahi hai.

**Prevention:** go-live se pehle har naya role aik asal user account
se test karein. Dekhein
[Lesson 09](../learn/framework/level-2/09-permissions-roles.md) aur
[Go-Live Checklist](go-live-checklist.md).

### B4 — "Data too long for column"

```text
pymysql.err.DataError: (1406, "Data too long for column 'remarks' at row 1")
```

**Kab hota hai:** Data field mein lambi value ke saath document save
karte waqt.

**Kyun hota hai:** **Data** field zyada se zyada 140 characters
rakhta hai. Form mein aap us se zyada type kar sakte hain, aur
database save karte waqt mana kar deta hai.

**Fix:** Customize Form mein field ka type **Small Text** kar dein
(65,535 characters tak), phir `bench --site <site> migrate` chalaye.

**Prevention:** Data sirf chhoti values ke liye use karein — naam,
code, phone number. Jo bhi cheez aik jumla ho sakti hai, woh shuru
se Small Text hai.

### B5 — Link validation fail / "Could not find"

```text
frappe.exceptions.LinkValidationError: Could not find Customer: Karachi Spice Traders
```

**Kab hota hai:** aisa document save karte waqt jis ka Link field
aisi document ki taraf ishara karta hai jo mojood hi nahi.

**Kyun hota hai:** linked document delete ya rename ho gayi, ya
value haath se type karte waqt typo ho gaya. Frappe latka hua link
save karne se mana karta hai — yeh validation ka kaam hai, bug nahi.

**Fix:**

1. Check karein ke linked document mojood hai: Desk mein use search
   karein.
2. Agar rename hui hai, to Link field ko naye naam par update karein.
3. Agar delete ho gayi hai, to use dobara banayein — ya field khaali
   chhod dein agar link optional hai.
4. Code mein link karne se pehle check karein:
   ```python
   if not frappe.db.exists("Customer", customer_name):
       frappe.throw(_("Customer {0} does not exist").format(customer_name))
   ```

**Prevention:** master (Customer, Item, Warehouse) kabhi delete na
karein jin ki taraf transactions ishara karte hon. Unhein cancel ya
disable karein, taake links resolve hote rahein.

### B6 — Save karte waqt mandatory field ka error

```text
frappe.exceptions.MandatoryError: [Sales Order, SO-0001]: posting_date
```

**Kab hota hai:** aisa document save karte waqt jo poora lagta hai —
har nazar aane wala field bhara hua hai.

**Kyun hota hai:** aik field mandatory mark hai lekin **Depends On**
condition ki wajah se chhupa hua hai, ya collapsed section mein
baitha hai. User use dekh hi nahi sakta, is liye bhar nahi sakta,
aur save mana kar deta hai.

**Fix:** DocType ke liye **Customize Form** kholein, mandatory field
dhoondhein, aur ya **Mandatory** tick hata dein ya **Depends On**
hata dein jo use chhupata hai. Aik field mandatory bhi ho aur
invisible bhi — yeh nahi ho sakta.

**Prevention:** jab bhi kisi field par Depends On lagayein, to usi
edit mein us ka Mandatory tick bhi check karein. Dekhein
[Common Mistakes](common-mistakes.md) guide.

### B7 — Server Script / Client Script chalti hi nahi

Koi error hi nahi — script bas kuch karti nahi.

**Kab hota hai:** aisi script likhne ke baad jo save, submit ya form
load par chalna chahiye.

**Kyun hota hai:** taqreeban hamesha chaar mein se aik wajah hoti
hai — script ghalat jagah par hai, event ka naam ghalat hai, change
ke baad DocType reload nahi hua, ya script mein khud aik error hai
jo sirf log mein nazar aata hai.

**Fix:**

1. Location check karein. Client behaviour DocType ki `.js` file
   mein hota hai, app mein
   (`<app>/<app>/doctype/<doctype>/<doctype>.js`); server behaviour
   `hooks.py` mein `doc_events` hook ya Server Script document mein
   hota hai — ulta nahi.
2. Event ka naam check karein: `validate` har save par chalta hai,
   `on_submit` sirf submit par, `refresh` form khulne par har dafa.
   Submit-only rule `validate` mein likhne se drafts bhi block ho
   jate hain.
3. DocType reload karein: `bench --site <site> migrate`, phir
   `bench --site <site> clear-cache` — aur Client Scripts ke liye
   `bench build` aur hard refresh (Ctrl+Shift+R).
4. Error dhoondhein: Client Scripts ke liye browser console (F12),
   Server Scripts ke liye Desk mein **Error Log**.

**Prevention:** aik script, aik event, aik file — aur use likhte hi
test karein, din ke end par nahi. Dekhein
[Lesson 05](../learn/framework/level-2/05-server-scripts-events.md)
aur [Lesson 06](../learn/framework/level-2/06-client-scripts.md).

### B8 — Print format purana output dikhata hai, ya blank PDF

**Kab hota hai:** Print Format edit karne ke baad, print hua document
abhi bhi purana layout dikhata hai — ya blank print hota hai.

**Kyun hota hai:** print output cache hota hai, aur format mein
Jinja error page par chup chaap fail ho jata hai jab ke asal error
log mein chala jata hai.

**Fix:**

1. Cache clear karein aur rebuild karein:
   ```bash
   bench --site <site> clear-cache
   bench build
   ```
2. Check karein ke Print Format DocType ke liye **Default** set hai,
   aur document waqai use hi use kar raha hai (Print → Format
   dropdown).
3. **Error Log** mein Jinja error check karein — blank print ki aam
   wajah format mein kharab `{{ }}` hoti hai.

**Prevention:** users ko batane se pehle print format aik asal
document par test karein. Dekhein
[Lesson 08](../learn/framework/level-2/08-reports-print-formats.md).

---

## Stage C — Production aur Go-Live

### C1 — "Something went wrong" / Internal Server Error

```text
Internal Server Error
Something went wrong. Please try again or contact support.
```

**Kab hota hai:** kisi bhi page par, kisi bhi waqt — aam tor par
deploy ya update ke foran baad.

**Kyun hota hai:** yeh message aik asal server error ka parda hai.
Wajah logs mein hoti hai, screen par kabhi nahi.

**Fix:**

1. Desk mein **Error Log** kholein — sab se nayi entry mein poora
   traceback hai. Uski aakhri line pehle parhein (upar wale checks
   dekhein).
2. Agar Desk khud down hai, to server par logs parhein:
   ```bash
   tail -50 logs/web.error.log
   tail -50 logs/frappe.log
   ```
3. Check karein ke disk full to nahi — full disk se healthy site par
   bhi random 500 errors aate hain:
   ```bash
   df -h
   ```

**Prevention:** backup aur rollback plan ke baghair Friday shaam ko
kabhi deploy na karein. Dekhein
[Go-Live Checklist](go-live-checklist.md).

### C2 — Scheduler chal hi nahi raha

Koi error message nahi — scheduled jobs, email aur reminders bas
kabhi hote hi nahi.

**Kab hota hai:** fresh production setup ke baad, restore ke baad,
ya jab kisi ne scheduler band kiya aur bhool gaya.

**Kyun hota hai:** scheduler har site ka alag switch hai. Agar woh
band hai, to koi scheduled job nahi chalta — sirf email nahi.
Production mein supervisor workers ka chalna bhi zaroori hai.

**Fix:**

```bash
bench --site <site> scheduler status
bench --site <site> enable-scheduler
bench doctor          # scheduler + workers aik jagah dikhata hai
```

Production mein workers bhi check karein:

```bash
sudo supervisorctl status
bench setup supervisor   # supervisor config missing ho to dobara banata hai
```

Aur check karein ke `sites/<site>/site_config.json` mein
`"pause_scheduler": 1` to nahi reh gaya — migration ya staging copy
se aksar reh jata hai.

**Prevention:** har deploy aur har reboot ke baad `bench doctor`
chalaye. Aik hafta band raha scheduler matlab aik hafta unsent mail
aur unrun jobs. Dekhein
[Lesson 11](../learn/framework/level-3/11-scheduler-jobs.md).

### C3 — Emails Email Queue mein phansi hui hain

**Kab hota hai:** mails **Email Queue** mein **Not Sent** ya
**Sending** status ke saath ghanton pari rehti hain — ya 2–5 minute
late aati hain.

**Kyun hota hai:** Frappe mail aap ke banate hi nahi bhejta. Aik
background job (`frappe.email.queue.flush`) entries har 4 minute mein
uthata hai, is liye kuch minute ki delay normal hai. Ghanton ka
matlab hai ke teen mein se aik cheez ghalat hai: sending suspend hai,
mail mute hai, ya scheduler chal nahi raha (dekhein C2).

**Fix:**

1. Desk mein **Email Queue** kholein. Agar upar right button par
   **Resume Sending** likha hai, to poori site ke liye sending band
   hai — use click karein.
2. `sites/<site>/site_config.json` mein `"mute_emails": 1` check
   karein — aam tor par testing ya staging copy se reh jata hai.
   Use hata dein aur bench restart karein.
3. Scheduler chal raha hai, yeh check karein (upar C2).
4. Queue haath se flush karke confirm karein ke kaam karta hai:
   ```bash
   bench --site <site> execute frappe.email.queue.flush
   ```
5. Fail hui entry ko us ke apne form se retry kiya ja sakta hai —
   use kholein aur **Send Now** use karein. Agar dobara fail ho, to
   us ka **Error** field parhein: woh asal problem batata hai
   (ghalat password, blocked port 25, ghalat SMTP host).

**Prevention:** har staging restore ke baad `mute_emails` check
karein, is se pehle ke koi soche ke mail kyun nahi aaya. Dekhein
[Lesson 12](../learn/framework/level-3/12-notifications-email.md).

### C4 — `bench update` fail: local changes overwrite ho jayengi

```text
error: Your local changes to the following files would be overwritten by merge
```

**Kab hota hai:** `bench update` karte waqt jab kisi ne server par
`apps/frappe` ya `apps/erpnext` ke andar files seedha edit ki hon.

**Kyun hota hai:** `bench update` naya code git se pull karta hai,
aur git aap ki badli hui files overwrite karne se mana karta hai.
Changes aam tor par accidental edit hoti hain — ya aik fix jo kisi ne
server par ki aur kahin commit nahi ki.

**Fix:**

1. Dekhein ke kya badla hai:
   ```bash
   git -C apps/frappe status --short
   git -C apps/erpnext status --short
   ```
2. Agar changes accidental hain, to stash karein aur update karein:
   ```bash
   git -C apps/frappe stash
   bench update
   ```
3. Agar woh aik asal fix hai, to pehle use apni app ya branch mein
   commit karein — `apps/frappe` ke andar uncommitted fix kabhi na
   chhodein.
4. `bench update --reset` local changes discard karke phir bhi update
   kar deta hai. Sirf tab use karein jab aap ko yaqeen ho ke changes
   disposable hain — yeh undo nahi ho sakta.

**Prevention:** server par framework ya ERPNext ka code kabhi seedha
edit na karein. Custom code aap ki apni app mein rehta hai; server ke
`apps/frappe` aur `apps/erpnext` saaf rehte hain.

### C5 — Backup restore kiya, site toot gayi / version mismatch

```text
pymysql.err.OperationalError: (1054, "Unknown column ...")
```

ya site load hoti hai lekin documents ghalat behave karte hain,
restore ke foran baad.

**Kab hota hai:** `bench --site <site> restore <backup>` ke baad,
khaas tor par jab backup doosre server ya version se aaya ho.

**Kyun hota hai:** backup data hota hai, code nahi. Restore karne se
purana data naye code ke neeche (ya ulta) aa jata hai, aur schema
tab tak match nahi karta jab tak migrate na chale. Agar apps backup
se mukhtalif major version par hain, to koi migrate use theek nahi
kar sakta.

**Fix:**

1. Restore ke baad hamesha migrate karein:
   ```bash
   bench --site <site> restore /path/to/backup.sql.gz
   bench --site <site> migrate
   ```
2. Check karein ke versions backup wali versions se match karte hain:
   ```bash
   bench version --format table
   ```
   Agar backup v15 ka hai aur bench v16 par hai, to pehle matching
   branches install karein
   (`bench get-app erpnext --branch version-15`), phir restore
   karein, phir migrate karein.
3. Agar restore khud fail ho, to check karein ke file bench backup
   hai (`.sql.gz`, `bench backup` se bani) aur restore ke liye free
   disk space hai.

**Prevention:** har backup par us ka version aur date likhein, aur
restore staging par test karein is se pehle ke aap ko asal mein
zaroorat pare. Dekhein
[Lesson 21](../learn/framework/level-4/21-ops.md).

### C6 — Bari reports par 504 Gateway Timeout

```text
504 Gateway Time-out
```

**Kab hota hai:** bari report chalate waqt, bulk import karte waqt,
ya browser se koi lamba kaam karte waqt.

**Kyun hota hai:** web request ki time limit hoti hai. Aik report jo
saal bhar ki Stock Ledger entries scan karti hai, ya das hazaar rows
ka import, limit se zyada waqt leta hai — server abhi bhi kaam kar
raha hota hai, lekin browser pehle hi haar maan chuka hota hai.

**Fix:**

1. Bhaari kaam web request mein na chalaye. Use background job mein
   bhej dein `frappe.enqueue` se — user ko jawab tab milta hai jab
   kaam poora ho, timeout nahi. Dekhein
   [Lesson 11](../learn/framework/level-3/11-scheduler-jobs.md).
2. Reports mein pehle filter lagayein: date range aur warehouse query
   chalne se pehle rows kam kar dete hain, baad mein nahi.
3. Log check karke confirm karein ke timeout tha, error nahi:
   ```bash
   tail -50 logs/web.log
   ```

**Prevention:** har woh kaam jo data ke saath barh sakta hai —
reports, imports, reconciliations — us din se background job mein
hona chahiye jis din woh likha gaya, pehle timeout ke baad nahi.
Dekhein [Lesson 14](../learn/framework/level-3/14-performance.md).

### C7 — Update ke baad Desk blank / assets 404

**Kab hota hai:** `bench update` ke baad, login page load hota hai
lekin Desk blank hai, ya browser console mein `.js` aur `.css` files
ke 404 dikhte hain.

**Kyun hota hai:** disk par built assets purane code ke hain, ya
browser purane assets pakde hue hai. Site theek hai; jo files woh
serve karti hai, woh stale hain.

**Fix:**

```bash
bench build
bench --site <site> clear-cache
```

Phir browser mein hard refresh karein (Ctrl+Shift+R). Agar
`bench build` khud fail ho, to dekhein A5 — aam tor par Node version
hi wajah hoti hai.

**Prevention:** har update `bench build` + `clear-cache` par khatam
hota hai, is se pehle ke aap users ko batayein ke site wapas aa gayi
hai. Use deploy checklist mein likhein, yaad mein nahi.

---

## Abhi bhi stuck hain?

1. Problem ko [Lesson 16 — Debugging](../learn/framework/level-3/16-debugging.md)
   ki tarah solve karein: console mein reproduce karein, sab se chhota
   case alag karein, traceback ki aakhri line parhein.
2. [Frappe Forum](https://discuss.frappe.io) par exact error text
   search karein — agar aap ko yeh hua hai, to kisi aur ko pehle hua
   hai.
3. Agar post karein, to chaar cheezein shamil karein warna koi madad
   nahi kar sakega: Frappe/ERPNext version (`bench version`), poora
   traceback (aakhri 20 lines), jab yeh hua to aap kya kar rahe the,
   aur is guide se aap ne pehle se kya try kiya hai.
4. Agar yeh framework ka bug lagta hai, to
   [frappe/frappe](https://github.com/frappe/frappe) par issue kholein
   — wohi chaar cheezein, aur minimal reproduction, apni poori site
   nahi.

## Hum isay kaise istemal kar sakte hain

Yeh woh page hai jo NexTash support client call par sab se pehle kholta
hai: client error parh kar sunata hai, hum use yahan dhoondhte hain,
aur fix aik ghante ki guessing ke baad nahi, minutes mein shuru ho jata
hai. Naye team members bhi isi tarah seekhte hain — har error jo unhein
pehli dafa hota hai, woh yahan pehle se likha hota hai, us fix ke saath
jo pichli dafa kaam kiya tha. Jab koi error is page par missing ho, to
woh signal hai ke use add karein: aik library jo har incident ke saath
barhti hai, us se zyada qeemti hai jo pehle din complete thi.

## Sources

Error messages aur fixes Frappe docs (Email Queue, password-reset
mail), Frappe Cloud docs (migrate out-of-memory, failed updates),
Frappe Forum, aur Frappe ke patch handler mein
`bench migrate --skip-failing` / `never_skip_patches` behaviour se
verify kiye gaye hain. Version requirements (v16: Python 3.14, Node
24, MariaDB 11.8) Frappe ke `pyproject.toml` dependency ranges se
liye gaye hain. Lesson links is hub ke apne lessons ki taraf ishara
karte hain.
