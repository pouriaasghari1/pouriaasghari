'use strict';
(() => {
 const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
 const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 const canvas=$('#fx-canvas');
 if(canvas&&!reduced&&window.matchMedia('(pointer:fine)').matches){
  const ctx=canvas.getContext('2d');let w=0,h=0,pts=[],trail=[],hue=185,raf;
  const resize=()=>{const dpr=Math.min(devicePixelRatio||1,1.6);w=innerWidth;h=innerHeight;canvas.width=w*dpr;canvas.height=h*dpr;canvas.style.width=w+'px';canvas.style.height=h+'px';ctx.setTransform(dpr,0,0,dpr,0,0);pts=Array.from({length:Math.min(54,Math.floor(w/25))},()=>({x:Math.random()*w,y:Math.random()*h,vx:(Math.random()-.5)*.22,vy:(Math.random()-.5)*.22,r:Math.random()*1.4+.3}));};
  resize();addEventListener('resize',resize,{passive:true});addEventListener('pointermove',e=>{trail.push({x:e.clientX,y:e.clientY,life:1,hue});if(trail.length>26)trail.shift();hue=(hue+2.2)%360},{passive:true});
  const draw=()=>{ctx.clearRect(0,0,w,h);for(let i=0;i<pts.length;i++){const p=pts[i];p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>w)p.vx*=-1;if(p.y<0||p.y>h)p.vy*=-1;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fillStyle='hsla('+(hue+i*2%60)+',90%,72%,.48)';ctx.fill();for(let j=i+1;j<pts.length;j++){const q=pts[j],d=Math.hypot(p.x-q.x,p.y-q.y);if(d<95){ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(q.x,q.y);ctx.strokeStyle='hsla('+hue+',90%,70%,'+((1-d/95)*.11)+')';ctx.lineWidth=.6;ctx.stroke()}}}trail.forEach((p,i)=>{p.life-=.045;const r=(i/trail.length)*6+1;ctx.beginPath();ctx.arc(p.x,p.y,r,0,Math.PI*2);ctx.fillStyle='hsla('+p.hue+',100%,70%,'+Math.max(0,p.life*.65)+')';ctx.fill()});trail=trail.filter(p=>p.life>0);raf=requestAnimationFrame(draw)};draw();
 }
 const transition=$('.transition-overlay');
 // Clear the page transition when the browser restores a page from its back/forward cache.
 // Without this, the opaque overlay can remain above the page until a manual refresh.
 const clearTransition=()=>{if(transition)transition.classList.remove('on');};
 window.addEventListener('pageshow',clearTransition);
 window.addEventListener('popstate',clearTransition);
 window.addEventListener('pagehide',()=>{if(transition)transition.classList.remove('on');});
 $('a[data-transition]').forEach(a=>a.addEventListener('click',e=>{
  if(e.defaultPrevented||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey||a.target==='_blank'||a.hasAttribute('download'))return;
  const href=a.getAttribute('href');
  if(!href||href.startsWith('#')||href.startsWith('mailto:')||href.startsWith('tel:'))return;
  const target=new URL(href,location.href);
  if(target.origin!==location.origin)return;
  // Same-document anchors should scroll normally instead of triggering a full-page overlay.
  if(target.pathname===location.pathname&&target.search===location.search){return;}
  e.preventDefault();
  if(transition&&!reduced)transition.classList.add('on');
  window.setTimeout(()=>{location.href=target.href;},reduced?0:180);
 }));
 const filterButtons=$('.filter-btn'),cards=$('.project-card[data-category]');
 // Scroll reveals: keep the page lively without hiding content if the API is unavailable.
 const revealItems=$('.home-page .reveal');
 cards.forEach(card=>card.classList.add('reveal'));
 if(!reduced&&'IntersectionObserver' in window){
  const revealObserver=new IntersectionObserver(entries=>entries.forEach(entry=>{
   if(entry.isIntersecting){entry.target.classList.add('is-visible');revealObserver.unobserve(entry.target);}
  }),{threshold:.12,rootMargin:'0px 0px -35px 0px'});
  $('.home-page .reveal').forEach(el=>revealObserver.observe(el));
 }else{
  $('.home-page .reveal').forEach(el=>el.classList.add('is-visible'));
 }
 filterButtons.forEach(btn=>btn.addEventListener('click',()=>{
  filterButtons.forEach(b=>{b.classList.toggle('active',b===btn);b.setAttribute('aria-pressed',String(b===btn));});
  const cat=btn.dataset.filter;
  cards.forEach(card=>{
   const visible=cat==='all'||card.dataset.category.split(' ').includes(cat);
   card.hidden=!visible;
   if(visible){card.classList.remove('is-visible');card.style.animation='none';void card.offsetWidth;card.style.animation='';requestAnimationFrame(()=>card.classList.add('is-visible'));}
  });
 }));
 cards.forEach(card=>card.addEventListener('pointermove',e=>{const r=card.getBoundingClientRect();card.style.setProperty('--mx',(e.clientX-r.left)+'px');card.style.setProperty('--my',(e.clientY-r.top)+'px')}));
 const page=document.body.dataset.project;if(page)mountProject(page);
 function mountProject(id){
  const mount=$('#project-app');if(!mount)return;
  const data={
   password:{title:'Password Generator',icon:'🔐',category:'ابزار کاربردی',desc:'یک رمز تصادفی با ترکیب حروف، عدد و نماد بساز.',tags:['Python concept','Random','Strings'],about:'نسخه تعاملی مرورگری برای تمرین random، رشته‌ها و انتخاب طول رمز.',tips:['طول رمز را بین ۸ تا ۶۴ انتخاب کن.','نوع کاراکترها را خودت تعیین کن.','رمز فقط در همین صفحه ساخته می‌شود و جایی ارسال نمی‌شود.']},
   hangman:{title:'Hangman',icon:'🔤',category:'بازی کلمه‌ای',desc:'کلمه انگلیسی مخفی را حرف‌به‌حرف حدس بزن.',tags:['Loops','Strings','Conditions'],about:'نسخه مرورگری بازی حدس کلمه؛ قواعد کلی آموزشی هستند و با فایل پایتون اصلی تطبیق‌سنجی نشده‌اند.',tips:['هر بار یک حرف انتخاب کن.','حداکثر ۶ حدس اشتباه داری.','برای شروع دوباره دکمه بازی جدید را بزن.']},
   rps:{title:'Rock Paper Scissors',icon:'✊',category:'بازی سریع',desc:'سنگ، کاغذ یا قیچی انتخاب کن و نتیجه را ببین.',tags:['Random','if / elif','Game logic'],about:'بازی کوتاه مبتنی بر انتخاب تصادفی رایانه و قوانین برد و باخت.',tips:['سنگ قیچی را می‌برد.','قیچی کاغذ را می‌برد.','کاغذ سنگ را می‌برد.']},
   adventure:{title:'Text Adventure',icon:'🏰',category:'داستان تعاملی',desc:'انتخاب‌هایت مسیر داستان را تغییر می‌دهند.',tags:['input','Conditions','Story'],about:'یک داستان شاخه‌ای کوتاه برای تمرین شرط‌ها و انتخاب مسیر.',tips:['توضیحات هر صحنه را بخوان.','یکی از انتخاب‌ها را بزن.','می‌توانی داستان را از اول شروع کنی.']},
   treasure:{title:'Treasure Map',icon:'🗺️',category:'بازی منطقی',desc:'روی نقشه نقطه‌ای را پیدا کن و گنج را کشف کن.',tags:['Lists','Coordinates','Logic'],about:'نسخه تعاملی تمرینی از بازی پیدا کردن گنج؛ محل گنج هر بار تصادفی است.',tips:['خانه‌های نقشه را انتخاب کن.','عدد فاصله راهنمایی‌ات می‌کند.','تلاش‌ها محدود هستند.']},
   coin:{title:'Coin Toss',icon:'◉',category:'بازی شانسی',desc:'شیر یا خط؟ سکه را بینداز و نتیجه را ببین.',tags:['Random','Choice','Probability'],about:'آزمایش ساده انتخاب تصادفی دو حالت سکه.',tips:['شیر یا خط را حدس بزن.','سکه را بینداز.','نتیجه‌ها صرفاً تصادفی هستند.']},
   bmi:{title:'BMI Calculator',icon:'🧮',category:'محاسبه‌گر',desc:'شاخص BMI را از روی قد و وزن حساب کن.',tags:['float','Formula','Input'],about:'محاسبه‌گر آموزشی؛ BMI به تنهایی معیار تشخیص سلامت یا توصیه پزشکی نیست.',tips:['قد را بر حسب سانتی‌متر وارد کن.','وزن را بر حسب کیلوگرم وارد کن.','نتیجه را فقط یک شاخص تقریبی در نظر بگیر.']},
   pizza:{title:'Pizza Order',icon:'▤',category:'محاسبه‌گر',desc:'سفارش نمونه را انتخاب کن و هزینه را حساب کن.',tags:['Variables','Conditions','Math'],about:'قیمت‌های این دمو فرضی‌اند و فروش واقعی یا پرداخت آنلاین انجام نمی‌شود.',tips:['اندازه و تعداد را انتخاب کن.','افزودنی‌ها را مشخص کن.','مبلغ نهایی به واحد فرضی نمایش داده می‌شود.']},
   love:{title:'Love Calculator',icon:'♡',category:'ابزار سرگرمی',desc:'یک نتیجه کاملاً سرگرمی و تصادفی تولید کن.',tags:['Strings','Random','Input'],about:'این ابزار صرفاً سرگرمی است و هیچ‌چیزی درباره رابطه واقعی افراد تعیین نمی‌کند.',tips:['دو نام وارد کن.','نتیجه تصادفی است.','آن را معیار واقعی رابطه در نظر نگیر.']},
   heights:{title:'Student Height Average',icon:'↕',category:'محاسبه‌گر',desc:'چند مقدار قد وارد کن و میانگین ریاضی را ببین.',tags:['Lists','Loops','Average'],about:'میانگین حسابی داده‌های واردشده را محاسبه می‌کند؛ برای رتبه‌بندی یا مقایسه افراد طراحی نشده است.',tips:['قدها را با ویرگول جدا کن.','مقادیر باید عدد مثبت باشند.','میانگین صرفاً نتیجه ریاضی داده‌هاست.']},
   coaster:{title:'Roller Coaster',icon:'⌁',category:'شرط‌ها و منطق',desc:'شرایط نمونه بلیت را بررسی کن و هزینه را ببین.',tags:['if / elif','Input','Conditions'],about:'یک سناریوی تمرینی با قوانین فرضی؛ محدودیت‌های واقعی هیچ شهربازی را نشان نمی‌دهد.',tips:['سن را وارد کن.','قد را بر حسب سانتی‌متر وارد کن.','قوانین نمونه را با قوانین واقعی اشتباه نگیر.']}
  }[id];
  if(!data){mount.innerHTML='<div class="result-box error">این پروژه پیدا نشد.</div>';return}
  document.title=data.title+' | Pouria Asghari';
  $('#project-title').textContent=data.title;$('#project-icon').textContent=data.icon;$('#project-category').textContent=data.category;$('#project-desc').textContent=data.desc;
  $('#project-tags').innerHTML=data.tags.map(t=>'<span class="side-tag"></span>').join('');$$('.side-tag',$('#project-tags')).forEach((el,i)=>el.textContent=data.tags[i]);
  $('#project-about').textContent=data.about;$('#project-tips').innerHTML=data.tips.map(t=>'<li></li>').join('');$$('li',$('#project-tips')).forEach((el,i)=>el.textContent=data.tips[i]);
  const button=(text,action,cls='button primary')=>'<button type="button" class="'+cls+'" data-action="'+action+'">'+text+'</button>';
  const field=(label,id,placeholder,type='text')=>'<div class="field"><label for="'+id+'">'+label+'</label><input id="'+id+'" type="'+type+'" placeholder="'+placeholder+'"></div>';
  const row=(...fields)=>'<div class="form-row">'+fields.join('')+'</div>';
  const actions=(...items)=>'<div class="game-buttons">'+items.join('')+'</div>';
  const result='<div class="result-box" id="game-result" aria-live="polite">نتیجه اینجا نمایش داده می‌شود.</div>';
  const game={
   password:()=>'<h2>ساخت رمز جدید</h2><p class="subtext">تنظیمات را انتخاب کن؛ رمز روی دستگاهت ساخته می‌شود.</p><div class="game-form">'+row(field('طول رمز (۸ تا ۶۴)','pw-len','16','number'))+'<div class="game-buttons"><label class="choice-btn"><input type="checkbox" id="pw-upper" checked> حروف بزرگ</label><label class="choice-btn"><input type="checkbox" id="pw-lower" checked> حروف کوچک</label><label class="choice-btn"><input type="checkbox" id="pw-num" checked> اعداد</label><label class="choice-btn"><input type="checkbox" id="pw-symbol" checked> نمادها</label></div>'+button('ساخت رمز','password')+result+'</div>',
   rps:()=>'<h2>انتخاب حرکت</h2><p class="subtext">حرکتت را انتخاب کن؛ رایانه هم یک حرکت تصادفی انتخاب می‌کند.</p><div class="game-visual"><div class="big-symbol" id="rps-visual">✊　✋　✌️</div></div>'+actions(button('✊ سنگ','rps-rock','choice-btn'),button('✋ کاغذ','rps-paper','choice-btn'),button('✌️ قیچی','rps-scissors','choice-btn'))+result+button('شروع دوباره','reset','button ghost'),
   hangman:()=>'<h2>کلمه مخفی را پیدا کن</h2><p class="subtext">هر حرف اشتباه، یک بخش از شکل نئونی را کامل می‌کند. با حدس درست، کلمه را نجات بده.</p><div class="game-visual"><div><svg id="hang-illustration" data-wrong="0" viewBox="0 0 220 190" role="img" aria-label="نمایش پیشرفت حدس‌ها"><g class="hang-scaffold"><path d="M25 172H145M55 172V18H128V35"/></g><g class="hang-person"><circle data-part="head" cx="128" cy="49" r="14"/><path data-part="body" d="M128 63V112"/><path data-part="arm-left" d="M128 76L106 96"/><path data-part="arm-right" d="M128 76L150 96"/><path data-part="leg-left" d="M128 112L108 140"/><path data-part="leg-right" d="M128 112L148 140"/></g></svg><div class="word-display" id="hang-word">_ _ _ _ _ _</div><p id="hang-status" class="subtext">۶ تلاش اشتباه در اختیار داری.</p></div></div><div class="letter-grid" id="hang-letters"></div>'+result+button('کلمه جدید','reset','button ghost'),
   adventure:()=>'<h2 id="story-title">دروازه سه‌راهی</h2><p class="subtext" id="story-copy">به یک قلعه قدیمی رسیده‌ای. دو مسیر پیش روی توست. انتخابت چیست؟</p>'+actions(button('ورود به جنگل','story-forest','choice-btn'),button('رفتن به غار','story-cave','choice-btn'))+result+button('شروع دوباره داستان','reset','button ghost'),
   treasure:()=>'<h2>نقشه گنج</h2><p class="subtext">گنج در یکی از خانه‌ها پنهان شده؛ عدد فاصله به تو کمک می‌کند.</p><div class="game-visual"><div class="treasure-grid" id="treasure-grid" style="display:grid;grid-template-columns:repeat(5,minmax(35px,1fr));gap:7px;width:min(100%,330px)"></div></div><p id="treasure-status" class="subtext">۵ تلاش داری.</p>'+result+button('نقشه جدید','reset','button ghost'),
   coin:()=>'<h2>شیر یا خط</h2><p class="subtext">قبل از انداختن سکه، حدست را انتخاب کن.</p>'+actions(button('شیر','coin-heads','choice-btn'),button('خط','coin-tails','choice-btn'))+'<div class="game-visual"><div class="big-symbol" id="coin-visual">◉</div></div>'+result,
   bmi:()=>'<h2>محاسبه شاخص BMI</h2><p class="subtext">واحدها را دقیق وارد کن؛ این نتیجه فقط محاسبه‌ای تقریبی است.</p><div class="game-form">'+row(field('قد (سانتی‌متر)','bmi-height','مثلاً 170','number'),field('وزن (کیلوگرم)','bmi-weight','مثلاً 65','number'))+button('محاسبه BMI','bmi')+result+'</div>',
   pizza:()=>'<h2>سفارش پیتزای نمونه</h2><p class="subtext">قیمت‌ها فرضی هستند و واحد پول واقعی ندارند.</p><div class="game-form"><div class="form-row"><div class="field"><label for="pizza-size">اندازه</label><select id="pizza-size"><option value="8">کوچک — ۸ واحد</option><option value="12" selected>متوسط — ۱۲ واحد</option><option value="16">بزرگ — ۱۶ واحد</option></select></div>'+field('تعداد','pizza-count','1','number')+'</div><div class="game-buttons"><label class="choice-btn"><input type="checkbox" id="pizza-cheese"> پنیر اضافه (+۲)</label><label class="choice-btn"><input type="checkbox" id="pizza-drink"> نوشیدنی (+۳)</label></div>'+button('محاسبه مبلغ سفارش','pizza')+result+'</div>',
   love:()=>'<h2>محاسبه‌گر سرگرمی نام‌ها</h2><p class="subtext">نتیجه ساختگی و تصادفی است و ارتباطی با سازگاری واقعی افراد ندارد.</p><div class="game-form">'+row(field('نام اول','love-a','نام اول'),field('نام دوم','love-b','نام دوم'))+button('ساخت نتیجه سرگرمی','love')+result+'</div>',
   heights:()=>'<h2>میانگین مجموعه اعداد</h2><p class="subtext">مقادیر را با ویرگول جدا کن؛ مثلاً ۱۶۰، ۱۷۲، ۱۶۸.</p><div class="game-form">'+field('مقادیر عددی','heights-values','160, 172, 168')+button('محاسبه میانگین','heights')+result+'</div>',
   coaster:()=>'<h2>بررسی قوانین نمونه بلیت</h2><p class="subtext">قوانین زیر صرفاً آموزشی هستند و برای هیچ مکان واقعی اعتبار ندارند.</p><div class="game-form">'+row(field('سن','coaster-age','مثلاً 16','number'),field('قد (سانتی‌متر)','coaster-height','مثلاً 150','number'))+button('بررسی شرایط نمونه','coaster')+result+'</div>'
  }[id];
  mount.innerHTML=game?game():'';
  let hangWord='',hangGuessed=[],hangWrong=0,treasurePos=0,treasureTries=5,coinChoice='';
  const show=(text,kind='')=>{const el=$('#game-result');if(el){el.textContent=text;el.className='result-box '+kind}};
  function initHang(){const list=['PYTHON','FUNCTION','VARIABLE','COMPUTER','RANDOM','PROGRAM'];hangWord=list[Math.floor(Math.random()*list.length)];hangGuessed=[];hangWrong=0;renderHang()}
  function renderHang(){const word=$('#hang-word');if(!word)return;word.textContent=hangWord.split('').map(c=>hangGuessed.includes(c)?c:'_').join(' ');const drawing=$('#hang-illustration');if(drawing)drawing.dataset.wrong=String(Math.min(hangWrong,6));$('#hang-status').textContent='تلاش اشتباه: '+hangWrong+' از ۶';const won=hangWord.split('').every(c=>hangGuessed.includes(c));$('#hang-letters').innerHTML='ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').map(l=>'<button class="letter-btn" data-letter="'+l+'" '+(hangGuessed.includes(l)||won||hangWrong>=6?'disabled':'')+'>'+l+'</button>').join('');if(won){show('برنده شدی! کلمه '+hangWord+' را پیدا کردی.','success');$('#hang-status').textContent='🎉 همه حروف درست پیدا شدند!'}else if(hangWrong>=6){show('این دور را باختی؛ کلمه درست «'+hangWord+'» بود. دوباره امتحان کن!','error');$('#hang-status').textContent='تلاش‌ها تمام شد؛ کلمه را یاد بگیر و دوباره بازی کن.'}else{show('ادامه بده؛ '+(6-hangWrong)+' تلاش باقی مانده.')}}
  function initTreasure(){treasurePos=Math.floor(Math.random()*25);treasureTries=5;$('#treasure-status').textContent='۵ تلاش داری.';$('#treasure-grid').innerHTML=Array.from({length:25},(_,i)=>'<button class="choice-btn" data-cell="'+i+'" style="padding:10px 0;min-width:0">?</button>').join('');show('یک خانه را برای پیدا کردن گنج انتخاب کن.')}
  function reset(){if(id==='hangman')initHang();if(id==='treasure')initTreasure();if(id==='adventure'){ $('#story-title').textContent='دروازه سه‌راهی';$('#story-copy').textContent='به یک قلعه قدیمی رسیده‌ای. دو مسیر پیش روی توست. انتخابت چیست؟';show('داستان از ابتدا شروع شد.')}if(id==='coin'){$('#coin-visual').textContent='◉';show('حدست را انتخاب کن.')}if(id==='rps'){$('#rps-visual').textContent='✊　✋　✌️';show('یک حرکت انتخاب کن.')} }
  mount.addEventListener('click',e=>{const letter=e.target.closest('[data-letter]');if(letter&&id==='hangman'){const l=letter.dataset.letter;if(!hangGuessed.includes(l)){hangGuessed.push(l);if(!hangWord.includes(l))hangWrong++;renderHang()}return}const cell=e.target.closest('[data-cell]');if(cell&&id==='treasure'&&!cell.disabled){const n=Number(cell.dataset.cell);treasureTries--;if(n===treasurePos){cell.textContent='★';cell.disabled=true;cell.style.color='var(--lime)';$$('[data-cell]',mount).forEach(b=>b.disabled=true);show('گنج را پیدا کردی! عالی بود.','success');$('#treasure-status').textContent='گنج پیدا شد.'}else{cell.textContent=String(Math.abs(Math.floor(n/5)-Math.floor(treasurePos/5))+Math.abs(n%5-treasurePos%5));cell.disabled=true;$('#treasure-status').textContent='تلاش باقی‌مانده: '+treasureTries;if(treasureTries===0){$$('[data-cell]',mount).forEach(b=>b.disabled=true);show('تلاش‌ها تمام شد؛ نقشه جدید را امتحان کن.','error')}}return}
  const b=e.target.closest('[data-action]');if(!b)return;const a=b.dataset.action;
  if(a==='reset'){reset();return}
  if(a==='password'){const n=Number($('#pw-len').value);let chars='';if($('#pw-upper').checked)chars+='ABCDEFGHIJKLMNOPQRSTUVWXYZ';if($('#pw-lower').checked)chars+='abcdefghijklmnopqrstuvwxyz';if($('#pw-num').checked)chars+='0123456789';if($('#pw-symbol').checked)chars+='!@#$%^&*_-+=';if(!Number.isInteger(n)||n<8||n>64){show('طول رمز باید عددی بین ۸ تا ۶۴ باشد.','error');return}if(!chars){show('حداقل یک گروه کاراکتر را انتخاب کن.','error');return}let out='';const cryptoObj=window.crypto;if(cryptoObj&&cryptoObj.getRandomValues){const buf=new Uint32Array(n);cryptoObj.getRandomValues(buf);for(let i=0;i<n;i++)out+=chars[buf[i]%chars.length]}else{for(let i=0;i<n;i++)out+=chars[Math.floor(Math.random()*chars.length)]}show(out,'success');return}
  if(a.startsWith('rps-')){const you=a.slice(4),opts=['rock','paper','scissors'],cpu=opts[Math.floor(Math.random()*3)],symbols={rock:'✊',paper:'✋',scissors:'✌️'},names={rock:'سنگ',paper:'کاغذ',scissors:'قیچی'};$('#rps-visual').textContent=symbols[you]+'　VS　'+symbols[cpu];const res=you===cpu?'مساوی شد!':((you==='rock'&&cpu==='scissors')||(you==='paper'&&cpu==='rock')||(you==='scissors'&&cpu==='paper'))?'تو بردی!':'رایانه برد!';show('انتخاب تو: '+names[you]+' — انتخاب رایانه: '+names[cpu]+' | '+res,you===cpu?'':res==='تو بردی!'?'success':'');return}
  if(a.startsWith('coin-')){coinChoice=a==='coin-heads'?'شیر':'خط';const out=Math.random()<.5?'شیر':'خط';$('#coin-visual').textContent=out==='شیر'?'🪙':'◉';show('حدس تو: '+coinChoice+' — نتیجه سکه: '+out+' | '+(coinChoice===out?'درست حدس زدی!':'این بار نشد.'),coinChoice===out?'success':'');return}
  if(a==='bmi'){const h=Number($('#bmi-height').value),w=Number($('#bmi-weight').value);if(h<50||h>260||w<10||w>400){show('لطفاً قد و وزن معتبر وارد کن.','error');return}show((w/((h/100)**2)).toFixed(1));return}
  if(a==='pizza'){const size=Number($('#pizza-size').value),count=Number($('#pizza-count').value);if(!Number.isInteger(count)||count<1||count>20){show('تعداد باید بین ۱ تا ۲۰ باشد.','error');return}const total=(size+($('#pizza-cheese').checked?2:0)+($('#pizza-drink').checked?3:0))*count;show('جمع سفارش: '+total+' واحد فرضی | تعداد: '+count,'success');return}
  if(a==='love'){const n1=$('#love-a').value.trim(),n2=$('#love-b').value.trim();if(!n1||!n2){show('هر دو نام را وارد کن.','error');return}show('نتیجه سرگرمی: '+(Math.floor(Math.random()*101))+'٪ — کاملاً تصادفی است و معنای واقعی ندارد.');return}
  if(a==='heights'){const raw=$('#heights-values').value.trim(),nums=raw.split(/[,،\s]+/).filter(Boolean).map(Number);if(!nums.length||nums.some(n=>!Number.isFinite(n)||n<=0)){show('فقط عددهای مثبت را با ویرگول جدا کن.','error');return}show('تعداد داده‌ها: '+nums.length+' | میانگین: '+(nums.reduce((s,n)=>s+n,0)/nums.length).toFixed(2),'success');return}
  if(a==='coaster'){const age=Number($('#coaster-age').value),height=Number($('#coaster-height').value);if(age<1||age>110||height<50||height>250){show('سن و قد معتبر وارد کن.','error');return}show(height>=120?'طبق قوانین فرضی این تمرین، شرط قد برقرار است.':'طبق قوانین فرضی این تمرین، شرط قد برقرار نیست.');return}
  if(a==='story-forest'){$('#story-title').textContent='مسیر جنگل';$('#story-copy').textContent='میان درختان یک صندوق می‌بینی؛ کلید زیر سنگی کنار رودخانه است.';show('پایان مسیر: کلید را پیدا کردی و صندوق را باز کردی.','success');return}
  if(a==='story-cave'){$('#story-title').textContent='مسیر غار';$('#story-copy').textContent='داخل غار دو چراغ می‌بینی و یک راه باریک در انتهاست.';show('پایان مسیر: چراغ را برداشتی و راه خروج را پیدا کردی.','success');return}
 });
 if(id==='hangman')initHang();if(id==='treasure')initTreasure();
 }
})();