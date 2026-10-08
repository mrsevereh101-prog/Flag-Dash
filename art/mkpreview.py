# Builds preview.html: the game with the 3D icons (img/icons/*.webp) in place of the emoji.
# index.html (the live game) is not touched.
import os, sys
REPO = '/home/user/Flag-Dash'
s = open(f'{REPO}/index.html', encoding='utf8').read()
ICONS = sorted(f[:-5] for f in os.listdir(f'{REPO}/img/icons') if f.endswith('.webp'))
assert len(ICONS) == 168, len(ICONS)

def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, (old[:90], n)
    s = s.replace(old, new)

IMG = lambda a: f'<img class="ico" src="img/icons/{a}.webp" alt="">'

# ---------- 1. the picture list and helpers ----------
rep("const EMOTES=['wave','flex','dance','point'];", """/* ---------- 3D icons: pictures in img/icons/<name>.webp take the place of the emoji ---------- */
const ICO=new Set('""" + ' '.join(ICONS) + """'.split(' '));
const ICO_KIND={item:k=>k==='swap'?'swap':'item_'+k,lo:k=>'lo_'+k,perk:k=>k==='swap'||k==='luck'?k:'perk_'+k,att:k=>'att_'+k,skin:k=>'skin_'+k,room:k=>k,trk:k=>'trk_'+k,rar:k=>'rar_'+k,
  rank:n=>/^world/i.test(n)?'rank_champs':'rank_'+String(n).toLowerCase(),power:h=>({samurai:'power_slash',warrior:'power_lightning',archer:'power_wind',elf:'power_trees',dwarf:'power_quake'})[h]};
const icoOf=(kind,id)=>{const a=id==null?'':ICO_KIND[kind](id);return a&&ICO.has(a)?a:'';};
const icoSrc=a=>'img/icons/'+a+'.webp';
const icoHTML=(a,cls)=>a?`<img class="ico${cls?' '+cls:''}" src="${icoSrc(a)}" alt="" draggable="false">`:'';
function icoEl(a,cls){const i=document.createElement('img');i.className='ico'+(cls?' '+cls:'');i.src=icoSrc(a);i.alt='';i.draggable=false;return i;}
const ICO_IMG={};const icoImg=a=>ICO_IMG[a]||(ICO_IMG[a]=Object.assign(new Image(),{src:icoSrc(a)}));
// show a picture in an icon box, or the emoji when there is no picture
function setIco(el,a,emoji){if(!el)return;if(a){if(el.dataset.ico!==a){el.dataset.ico=a;el.textContent='';el.appendChild(icoEl(a));}}else{delete el.dataset.ico;el.textContent=emoji||'';}}
// pictures for the emoji used in the race feed
const HIT_ICO={'🚀':'item_rocket','🍌':'item_banana','💣':'item_mine','🔥':'item_fire','❄️':'item_freeze','⚡':'power_lightning','⚔️':'power_slash','🌋':'power_quake','🌪️':'power_wind','🌳':'power_trees','🎯':'lo_dart','🕸️':'lo_net','☄️':'lo_meteor','💥':'lo_shock','🌀':'lo_vortex','👻':'item_ghost','🛡️':'item_shield','🔄':'swap','🧿':'perk_nullify'};
const hitIco=ic=>HIT_ICO[ic]&&ICO.has(HIT_ICO[ic])?HIT_ICO[ic]:'';
const EMOTES=['wave','flex','dance','point'];""")

# ---------- 2. menu squares ----------
rep("  if(o.img){o.img.classList.add('tile-img');b.appendChild(o.img);}else if(o.html){",
    "  if(o.ico){b.appendChild(icoEl(o.ico,'col-art'));}else if(o.img){o.img.classList.add('tile-img');b.appendChild(o.img);}else if(o.html){")
# store
rep("      let o;if(storeTab==='skins'){o=it.hero?{img:heroTileImg(it.hero,it.id),label:it.name}:{html:skin3D(it),label:it.name};}\n      else{o={icon:it.icon",
    "      let o;if(storeTab==='skins'){const sa=icoOf('skin',it.id);o=sa?{ico:sa,label:it.name}:it.hero?{img:heroTileImg(it.hero,it.id),label:it.name}:{html:skin3D(it),label:it.name};}\n      else{o={ico:icoOf(storeTab==='items'?'lo':storeTab==='attire'?'att':'perk',it.id),icon:it.icon")
rep("h.className='tier-head rh-'+t.id;h.textContent=t.name;grid.appendChild(h);",
    "h.className='tier-head rh-'+t.id;h.textContent=t.name;{const ra=icoOf('rar',t.id);if(ra)h.prepend(icoEl(ra,'rar-ico'));}grid.appendChild(h);")
# owned
rep("k=>k.hero?{img:heroTileImg(k.hero,k.id),label:k.name}:{html:skin3D(k),label:k.name},skinCard,'skin');",
    "k=>icoOf('skin',k.id)?{ico:icoOf('skin',k.id),label:k.name}:k.hero?{img:heroTileImg(k.hero,k.id),label:k.name}:{html:skin3D(k),label:k.name},skinCard,'skin');")
rep("l=>({icon:l.icon,label:l.name}),itemCard,'item');", "l=>({ico:icoOf('lo',l.id),icon:l.icon,label:l.name}),itemCard,'item');")
rep("a=>({icon:a.icon,label:a.name}),attireCard,'att');", "a=>({ico:icoOf('att',a.id),icon:a.icon,label:a.name}),attireCard,'att');")
rep("b=>b.id==='luck'?{icon:'🍀',label:b.name}:{icon:BUFF_ICON[b.id],label:b.name,",
    "b=>b.id==='luck'?{ico:icoOf('perk','luck'),icon:'🍀',label:b.name}:{ico:icoOf('perk',b.id),icon:BUFF_ICON[b.id],label:b.name,")
# loadout picker
rep("el:mkTile({icon:l.icon,label:l.name,cls:(on?'on ':'')", "el:mkTile({ico:icoOf('lo',l.id),icon:l.icon,label:l.name,cls:(on?'on ':'')")
# perk picker and the perk button
rep("if(ic)ic.textContent=p?BUFF_ICON[p.id]:'⭐';", "setIco(ic,p?icoOf('perk',p.id):'',p?BUFF_ICON[p.id]:'⭐');")
rep("if(luckActive()){if(ic)ic.textContent='🍀';", "if(luckActive()){setIco(ic,icoOf('perk','luck'),'🍀');")
rep("el:mkTile({icon:'🍀',label:'Lucky Clover',", "el:mkTile({ico:icoOf('perk','luck'),icon:'🍀',label:'Lucky Clover',")
rep("el:mkTile({icon:BUFF_ICON[b.id],label:b.name,badge:n?", "el:mkTile({ico:icoOf('perk',b.id),icon:BUFF_ICON[b.id],label:b.name,badge:n?")
# loadout button on the race desk
rep("$('pkLoadIc').textContent=m?m[1]:'🎒';", "setIco($('pkLoadIc'),loOn?icoOf('lo',wallet.lo.atk):'',m?m[1]:'🎒');")
# track button on the race desk
rep('<i aria-hidden="true">🛣️</i><b id="pkTrack">', '<i aria-hidden="true" id="pkTrackIc">🛣️</i><b id="pkTrack">')
rep("$('pkTrack').textContent=themeById(selTrack).name;", "$('pkTrack').textContent=themeById(selTrack).name;setIco($('pkTrackIc'),icoOf('trk',selTrack),'🛣️');")
# track picker
rep("el:mkTile({html:art,label:th.name,", "el:mkTile({ico:icoOf('trk',th.id),html:art,label:th.name,")
# room: spot picker, gift picker, collection, item list
rep("el:mkTile({icon:it.ic,label:it.name,cls:cur===it.id?'on own':'own',badge:'💪'+it.pw})",
    "el:mkTile({ico:icoOf('room',it.id),icon:it.ic,label:it.name,cls:cur===it.id?'on own':'own',badge:'💪'+it.pw})")
rep("el:mkTile({icon:it.ic,label:it.name,cls:ok?'own':'locked'})", "el:mkTile({ico:icoOf('room',it.id),icon:it.ic,label:it.name,cls:ok?'own':'locked'})")
rep("const ic=document.createElement('span');ic.className='col-ic';ic.textContent=it.ic;b.appendChild(ic);",
    "const ra=icoOf('room',it.id);if(ra)b.appendChild(icoEl(ra,'col-art'));else{const ic=document.createElement('span');ic.className='col-ic';ic.textContent=it.ic;b.appendChild(ic);}")
rep("const ic=document.createElement('span');ic.className='ri-ic';ic.textContent=it.ic;", "const ic=document.createElement('span');ic.className='ri-ic';setIco(ic,icoOf('room',it.id),it.ic);")

# ---------- 3. race HUD ----------
rep("$('atkIcon').textContent=A.icon;", "setIco($('atkIcon'),icoOf('lo',A.id),A.icon);")
rep("$('defIcon').textContent=D.icon;", "setIco($('defIcon'),icoOf('lo',D.id),D.icon);")
rep("$('itemIcon').textContent=it?ITEMS[it].icon:'';", "setIco($('itemIcon'),it?icoOf('item',it):'',it?ITEMS[it].icon:'');")
rep("const w=document.createElement('span');w.className='hc-ic';w.textContent=ic;e.append(im(a),w,im(b));",
    "const w=document.createElement('span');w.className='hc-ic';setIco(w,hitIco(ic),ic);e.append(im(a),w,im(b));")
rep("const w=document.createElement('span');w.className='hc-ic';w.textContent=ic;e.appendChild(w);",
    "const w=document.createElement('span');w.className='hc-ic';setIco(w,hitIco(ic),ic);e.appendChild(w);")

# ---------- 4. rewards: chest, Congratulations card, race celebration ----------
rep("const CHEST_KIND={'🪙':'gold','💎':'silver','⭐':'gold'};",
    """const CHEST_KIND={'🪙':'gold','💎':'silver','⭐':'gold'};
const CHEST_ICO=[[/xp|rank/i,'xp'],[/daily|task/i,'task'],[/leaderboard/i,'menu_boards'],[/grand prix/i,'gp_points'],[/best/i,'stopwatch'],[/hit|stole/i,'lo_shock'],[/room|trophy|medal|monument/i,'cup_gold']];
function noteIco(n){const sk=/skin|unlock/i.test(n)&&SKINS_SHOP.find(k=>n.includes(k.name));if(sk)return icoOf('skin',sk.id);const ri=ROOM_ITEMS.find(i=>n.includes(i.name));if(ri)return icoOf('room',ri.id);
  const m=CHEST_ICO.find(([re])=>re.test(n));return ICO.has(m?m[1]:'g_box')?(m?m[1]:'g_box'):'';}""")
rep("const items=[{ic:'🪙',big:'+'+(coins|0),t:'Coins'}];if(gems)items.push({ic:'💎',big:'+'+gems,t:gems>1?'Diamonds':'Diamond'});",
    "const items=[{ic:'🪙',ico:'coin',big:'+'+(coins|0),t:'Coins'}];if(gems)items.push({ic:'💎',ico:'gem',big:'+'+gems,t:gems>1?'Diamonds':'Diamond'});")
rep("items.push({ic:(CHEST_IC.find(([re])=>re.test(n))||[0,'🎁'])[1],big:", "items.push({ic:(CHEST_IC.find(([re])=>re.test(n))||[0,'🎁'])[1],ico:noteIco(n),big:")
rep("const sp=document.createElement('span');sp.textContent=it.ic;", "const sp=document.createElement('span');if(it.ico)sp.appendChild(icoEl(it.ico));else sp.textContent=it.ic;")
rep("i.className='cg-ic';i.textContent=it.ic;", "i.className='cg-ic';setIco(i,it.ico,it.ic);")
rep("gifts.push({ic:'🎁',v:priceHTML(rw.coinsWon,'coin'),l:'Coins earned'});", "gifts.push({ic:'🎁',ico:'coin',v:priceHTML(rw.coinsWon,'coin'),l:'Coins earned'});")
rep("if(rw.gemsWon)gifts.push({ic:'💎',", "if(rw.gemsWon)gifts.push({ic:'💎',ico:'gem',")
rep("gifts.push({ic:place===1?'🏆':place<=3?'🏅':'🎽',", "gifts.push({ic:place===1?'🏆':place<=3?'🏅':'🎽',ico:place===1?'cup_gold':place<=3?'m_podium':'',")
rep("gifts.push({ic:'📈',", "gifts.push({ic:'📈',ico:'gp_points',")
rep("gifts.push({ic:RACE.roomNew[0].ic,", "gifts.push({ic:RACE.roomNew[0].ic,ico:icoOf('room',RACE.roomNew[0].id),")
rep("if(rw.firstSkin)gifts.push({ic:'👕',", "if(rw.firstSkin)gifts.push({ic:'👕',ico:icoOf('skin',rw.firstSkin.id),")
rep("gifts.push({ic:'💥',", "gifts.push({ic:'💥',ico:'lo_shock',")
rep("if(rw.lv)gifts.push({ic:rw.lv.to>rw.lv.from?'🆙':'⭐',", "if(rw.lv)gifts.push({ic:rw.lv.to>rw.lv.from?'🆙':'⭐',ico:rw.lv.to>rw.lv.from?icoOf('rank',rankOf(rw.lv.to).n):'xp',")
rep("gifts.push({ic:'🔓',v:rw.lv.unlocked[0],", "gifts.push({ic:'🔓',ico:icoOf('skin',(SKINS_SHOP.find(k=>k.name===rw.lv.unlocked[0])||{}).id),v:rw.lv.unlocked[0],")
rep('d.innerHTML=`<span class="gbox">${x.ic}</span>', 'd.innerHTML=`<span class="gbox">${x.ico?icoHTML(x.ico):x.ic}</span>')

# ---------- 5. level and ranks ----------
rep("el.querySelector('b').textContent=rk.ic+' '+rk.n+' '+rk.step;",
    "{const bb=el.querySelector('b');bb.textContent=rk.n+' '+rk.step;const ra=icoOf('rank',rk.n);bb.prepend(ra?icoEl(ra,'rk-ico'):rk.ic+' ');}")
rep("h.className='lv-tier';h.textContent=rk.ic+' '+rk.n+` (${rk.n==='Track'?'1':rk.step}–${RANKS.find(x=>x.n===rk.n).k})`;box.appendChild(h);",
    "h.className='lv-tier';h.textContent=rk.n+` (${rk.n==='Track'?'1':rk.step}–${RANKS.find(x=>x.n===rk.n).k})`;{const ra=icoOf('rank',rk.n);h.prepend(ra?icoEl(ra,'rk-ico'):rk.ic+' ');}box.appendChild(h);")
rep("h.className='lv-tier soon';h.textContent=`${t.ic} ${t.n}: coming soon`;box.appendChild(h);",
    "h.className='lv-tier soon';h.textContent=`${t.n}: coming soon`;{const ra=icoOf('rank',t.n);h.prepend(ra?icoEl(ra,'rk-ico'):t.ic+' ');}box.appendChild(h);")
rep("if(sk){const sw=document.createElement('i');sw.style.background=sk.sw;row.append(n,sw,d);}",
    "if(sk){const sa=icoOf('skin',sk.id);const sw=sa?icoEl(sa,'lv-sk'):document.createElement('i');if(!sa)sw.style.background=sk.sw;row.append(n,sw,d);}")

# ---------- 6. results header: the track's island instead of a mascot ----------
rep("h.dataset.art=TRACK_ART[TH.id]||'🏁';}",
    "h.dataset.art=TRACK_ART[TH.id]||'🏁';const ta=icoOf('trk',TH.id);h.classList.toggle('has-trk',!!ta);if(ta)h.style.setProperty('--trk-img',`url(${icoSrc(ta)})`);}")

# ---------- 7. trophy room: 3D pictures on the spots and on the screens ----------
rep("  emo(ic){return canvasTex(", "  icoTex(a){if(!a)return null;const c=this.icoCache||(this.icoCache={});if(!c[a]){const t=new THREE.TextureLoader().load(icoSrc(a));t.encoding=THREE.sRGBEncoding;t.anisotropy=MAXANISO;t.__keep=true;c[a]=t;}return c[a];},\n  emo(ic){return canvasTex(")
rep("map:this.emo(it.ic),transparent:true,depthWrite:false}));sp.scale.set(sl.sz,sl.sz,1);",
    "map:this.icoTex(icoOf('room',it.id))||this.emo(it.ic),transparent:true,depthWrite:false,toneMapped:false}));sp.scale.set(sl.sz,sl.sz,1);")
rep("if(p)out.push({ic:BUFF_ICON[p.id],", "if(p)out.push({ic:BUFF_ICON[p.id],ico:icoOf('perk',p.id),")
rep("out.push({ic:BUFF_ICON[b.id],top:b.name,sub:`Perk ×${n}`});", "out.push({ic:BUFF_ICON[b.id],ico:icoOf('perk',b.id),top:b.name,sub:`Perk ×${n}`});")
rep("if(A)out.push({ic:A.icon,top:A.name,sub:'Attack'});if(D)out.push({ic:D.icon,top:D.name,sub:'Defence'});",
    "if(A)out.push({ic:A.icon,ico:icoOf('lo',A.id),top:A.name,sub:'Attack'});if(D)out.push({ic:D.icon,ico:icoOf('lo',D.id),top:D.name,sub:'Defence'});")
rep("if(a)out.push({ic:a.icon,top:a.name,", "if(a)out.push({ic:a.icon,ico:icoOf('att',a.id),top:a.name,")
rep("out.push({ic:'👕',top:k.name,sub:'Skin'});", "out.push({ic:'👕',ico:icoOf('skin',id),top:k.name,sub:'Skin'});")
rep("[{ic:'⭐',top:skinById(mySkinId()).name,sub:'Equipped',col:'#5fd08a'}]", "[{ic:'⭐',ico:icoOf('skin',mySkinId()),top:skinById(mySkinId()).name,sub:'Equipped',col:'#5fd08a'}]")
rep(".map(id=>({ic:'👕',top:skinById(id).name,sub:'Owned'}))", ".map(id=>({ic:'👕',ico:icoOf('skin',id),top:skinById(id).name,sub:'Owned'}))")
rep("""c.font='54px "Apple Color Emoji","Segoe UI Emoji","Noto Color Emoji",sans-serif';c.fillText(r.ic,26,y);""",
    """const im=r.ico&&icoImg(r.ico);if(im&&im.complete&&im.naturalWidth)c.drawImage(im,14,y-42,84,84);else{c.font='54px "Apple Color Emoji","Segoe UI Emoji","Noto Color Emoji",sans-serif';c.fillText(r.ic,26,y);}""")
rep("    if(mesh.material.map)mesh.material.map.dispose();mesh.material.map=t;mesh.material.needsUpdate=true;},",
    """    if(mesh.material.map)mesh.material.map.dispose();mesh.material.map=t;mesh.material.needsUpdate=true;
    // pictures still loading: draw the screen again once they arrive
    const wait=(rows||[]).filter(r=>r.ico).map(r=>icoImg(r.ico)).filter(im=>!im.complete);
    if(wait.length&&!mesh.__icoWait){mesh.__icoWait=true;Promise.all(wait.map(im=>new Promise(res=>{im.addEventListener('load',res,{once:true});im.addEventListener('error',res,{once:true});}))).then(()=>{mesh.__icoWait=false;this.drawScreen(mesh,title,rows,wide);});}},""")
rep("$('roomEdit').textContent=RV.edit?'✓ Done':'✏️ Decorate';", "$('roomEdit').innerHTML=RV.edit?'✓ Done':icoHTML('decorate')+' Decorate';")

# ---------- 8. buttons in the page itself ----------
rep('aria-label="My room" title="My room">🏠</button>', 'aria-label="My room" title="My room">' + IMG('menu_room') + '</button>')
rep('id="deskSet" aria-label="Settings">⚙</button>', 'id="deskSet" aria-label="Settings">' + IMG('menu_settings') + '</button>')
rep('id="deskStore" aria-label="Store" title="Store">🛒</button>', 'id="deskStore" aria-label="Store" title="Store">' + IMG('menu_store') + '</button>')
rep('id="deskBoards" aria-label="Leaderboards" title="Leaderboards">🏟️</button>', 'id="deskBoards" aria-label="Leaderboards" title="Leaderboards">' + IMG('menu_boards') + '</button>')
rep('title="Friends and inbox">✉️</button>', 'title="Friends and inbox">' + IMG('menu_inbox') + '</button>')
rep('id="d3Store" aria-label="Store">🛒</button>', 'id="d3Store" aria-label="Store">' + IMG('menu_store') + '</button>')
rep('aria-label="Emotes">🙌</button>', 'aria-label="Emotes">' + IMG('emotes') + '</button>')
rep('aria-controls="paneQuick"><i>🏁</i>', 'aria-controls="paneQuick"><i>' + IMG('tab_quick') + '</i>')
rep('aria-controls="paneOnline"><i>🌐</i>', 'aria-controls="paneOnline"><i>' + IMG('tab_online') + '</i>')
rep('aria-controls="paneSolo"><i>🏆</i>', 'aria-controls="paneSolo"><i>' + IMG('tab_challenges') + '</i>')
rep('<span class="d3-qic">🏁</span>', '<span class="d3-qic">' + IMG('tab_quick') + '</span>')
rep('id="roomColBtn">📖 Collection</button>', 'id="roomColBtn">' + IMG('collection') + ' Collection</button>')
rep('id="roomEdit">✏️ Decorate</button>', 'id="roomEdit">' + IMG('decorate') + ' Decorate</button>')
rep('id="menuChatBtn">💬 Chat</button>', 'id="menuChatBtn">' + IMG('chat') + ' Chat</button>')
rep('id="menuGuildBtn">Guild</button>', 'id="menuGuildBtn">' + IMG('guild') + ' Guild</button>')
rep('<span class="d3-gem">💎 <b id="d3Gems">0</b></span>', '<span class="d3-gem"><span class="gem-ic"></span> <b id="d3Gems">0</b></span>')

# ---------- 8b. smaller leftovers ----------
rep('<span class="muted">Profiles show each course\'s elevation</span>', '<span class="muted">Tap a track for its details</span>')
rep('<b>🏠 My Room</b>', '<b>' + IMG('menu_room') + ' My Room</b>')
rep('<span>💪</span><b id="roomStr">', '<span>' + IMG('strength') + '</span><b id="roomStr">')
rep('<h2 id="rcTitle">📖 Room collection</h2>', '<h2 id="rcTitle">' + IMG('collection') + ' Room collection</h2>')
rep('<button data-act="emote" aria-label="Emote">🙌</button>', '<button data-act="emote" aria-label="Emote">' + IMG('emotes') + '</button>')
rep("COL_CATS.forEach(([id,nm])=>{const b=document.createElement('button');b.textContent=nm;",
    "COL_CATS.forEach(([id,nm])=>{const b=document.createElement('button');const ca=icoOf('room',{trophy:'cup_gold',medal:'m_podium',monument:'mon_hall',furniture:'f_couch',decor:'d_poster',gift:'g_box'}[id]);if(ca){b.textContent=nm.replace(/^\\S+\\s+/,'');b.prepend(icoEl(ca,'tab-ico'));}else b.textContent=nm;")
rep("st.textContent='💪 '+roomStrength();", "{st.textContent=' '+roomStrength();if(ICO.has('strength'))st.prepend(icoEl('strength','st-ico'));else st.textContent='💪'+st.textContent;}")
# info cards: a picture next to the name; skins get a big picture on top
rep("card.querySelector('.shop-name').textContent=(it.icon?it.icon+' ':'')+it.name;",
    "{const sn=card.querySelector('.shop-name'),a=LOADOUT.includes(it)?icoOf('lo',it.id):ATTIRE.includes(it)?icoOf('att',it.id):(BUFFS.includes(it)||it===LUCK)?icoOf('perk',it.id):'';sn.textContent=(a||!it.icon?'':it.icon+' ')+it.name;if(a)sn.prepend(icoEl(a,'sn-ico'));}")
rep("const card=shopCard(s,s.hero?'':`<div class=\"sk3d big\">",
    "const card=shopCard(s,icoOf('skin',s.id)?`<div class=\"sk-big\">${icoHTML(icoOf('skin',s.id))}</div>`:s.hero?'':`<div class=\"sk3d big\">")

# ---------- 9. styles for the pictures ----------
CSS = """<style id="icoStyle">
/* 3D icons */
.ico{display:block;width:1.3em;height:1.3em;object-fit:contain;pointer-events:none;-webkit-user-drag:none;user-select:none}
.col-sq .col-art{width:64%;height:64%;filter:drop-shadow(0 3px 3px rgba(0,0,0,.35))}
.tile.has-lb .col-art{margin-bottom:12px}
.col-sq.locked .col-art{filter:grayscale(1) brightness(.8);opacity:.55}
.coin-ic{background:url(img/icons/coin.webp) center/contain no-repeat!important;box-shadow:none!important;border-radius:0!important;width:18px!important;height:18px!important;vertical-align:-4px}
.gem-ic{background:url(img/icons/gem.webp) center/contain no-repeat!important;border-radius:0!important;width:17px!important;height:17px!important;transform:none;margin:0 2px;vertical-align:-3px}
.d3-round .ico{width:82%;height:82%}
.d3-emote-ic .ico{width:80%;height:80%}
.d3-tabbar i .ico{width:32px;height:32px;margin:0 auto}
.pick-btn i .ico{width:1.5em;height:1.5em}
.slot-icon .ico{width:88%;height:88%}
.ri-ic .ico{width:38px;height:38px;margin:0 auto}
.cg-ic .ico{width:42px;height:42px}
.cel-gift .gbox .ico{width:42px;height:42px;margin:0 auto}
.hc-ic .ico{width:26px;height:26px}
.ch-pops span .ico{width:36px;height:36px}
.tier-head .rar-ico{width:22px;height:22px}
.d3-qic .ico{width:46px;height:46px}
#roomColBtn .ico,#roomEdit .ico,#menuChatBtn .ico,#menuGuildBtn .ico{display:inline-block;width:22px;height:22px;vertical-align:-5px}
.lv-badge b .rk-ico{display:inline-block;width:20px;height:20px;vertical-align:-5px;margin-right:3px}
.lv-tier .rk-ico{display:inline-block;width:28px;height:28px;vertical-align:-8px;margin-right:6px}
.lv-row .lv-sk{width:30px;height:30px;flex:none}
html.cream.adv .lv-shield{background:url(img/icons/lv_shield.webp) center/contain no-repeat!important;clip-path:none!important;color:#fff;text-shadow:0 1px 2px rgba(80,50,0,.8)}
#results .board-head.has-trk::after{content:'';width:96px;height:96px;bottom:-14px;background:var(--trk-img) center/contain no-repeat}
.rh-title b .ico{display:inline-block;width:26px;height:26px;vertical-align:-5px}
.rh-str span .ico{width:26px;height:26px}
#rcTitle .ico{display:inline-block;width:30px;height:30px;vertical-align:-7px}
#rcTabs .tab-ico{display:inline-block;width:20px;height:20px;vertical-align:-4px;margin-right:4px}
.lv-badge em .st-ico{display:inline-block;width:15px;height:15px;vertical-align:-3px}
.shop-name .sn-ico{display:inline-block;width:30px;height:30px;vertical-align:-8px;margin-right:6px}
.sk-big{display:grid;place-items:center;height:124px}.sk-big .ico{width:124px;height:124px;filter:drop-shadow(0 6px 6px rgba(0,0,0,.35))}
.tgroup button .ico{width:66%;height:66%;margin:auto}
#storeGrid>.tgrid{grid-column:1/-1}
#icoTag{position:fixed;left:6px;bottom:calc(6px + env(safe-area-inset-bottom,0px));z-index:9999;font:700 11px/1.4 system-ui,sans-serif;background:#2a7fd0;color:#fff;padding:2px 8px;border-radius:9px;opacity:.85;pointer-events:none}
</style>
</head>"""
rep('</head>', CSS)
rep('</body>', '<div id="icoTag">3D icons preview</div>\n</body>')

open(f'{REPO}/preview.html', 'w', encoding='utf8').write(s)
print('preview.html written,', len(s), 'chars;', len(ICONS), 'icons')
