const test=require('node:test'),assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs');
const source=fs.readFileSync('assets/analytics-consent.js','utf8');
function context(choice){
 const listeners={},appended=[];
 const document={referrer:'https://example.invalid/article?email=private@example.invalid',readyState:'loading',cookie:'',head:{appendChild:e=>appended.push(e)},addEventListener:(event,cb)=>listeners[event]=cb};
 document.createElement=tag=>({tag,dataset:{}});
 const window={};const context={window,document,location:{protocol:'https:',origin:'https://angsumi.online',pathname:'/inquiry/'},localStorage:{getItem:()=>choice?choice+':'+Date.now():null},URL,Date,encodeURIComponent};
 vm.runInNewContext(source,context);return {window,appended};
}
test('no GA or custom event before consent',()=>{for(const choice of [null,'rejected']){const {window,appended}=context(choice);window.angsumiTrackBusiness('generate_lead',{category:'research'});assert.equal(appended.length,0);assert.equal(window.dataLayer,undefined);}});
test('only fixed event values and closed context vocabularies',()=>{const {window}=context('accepted');window.angsumiTrackBusiness('generate_lead',{category:'research',campaign:'research-checklist',email:'private@example.invalid',name:'Secret Person'});window.angsumiTrackBusiness('generate_lead',{category:'private@example.invalid',campaign:'Secret Person'});window.angsumiTrackBusiness('private_event',{category:'research'});const events=window.dataLayer.map(args=>Array.from(args));const leads=events.filter(args=>args[0]==='event'&&args[1]==='generate_lead');assert.equal(leads.length,2);assert.equal(leads[0][2].service_category,'research');assert.equal(leads[1][2].service_category,'other');assert.equal(leads[1][2].resource_campaign,'none');assert.ok(!JSON.stringify(events).includes('private@example.invalid'));assert.ok(!JSON.stringify(events).includes('Secret Person'));assert.ok(!JSON.stringify(events).includes('?email='));});
