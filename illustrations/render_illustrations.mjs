import {createRequire} from 'node:module';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const root=join(dirname(fileURLToPath(import.meta.url)),'..','docs','illustrations');
const modules=process.env.SUPPORT_NODE_MODULES;
const require=modules?createRequire(join(modules,'loader.js')):createRequire(import.meta.url);
const sharp=require('sharp');
const manifest=JSON.parse(await readFile(join(root,'manifest.json'),'utf8'));
const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
await mkdir(join(root,'book'),{recursive:true});
for(const f of manifest.figures){
  await sharp(join(root,f.slug+'.svg'),{density:156}).resize(1950,1333).png().withMetadata({density:300}).toFile(join(root,f.slug+'.png'));
  await sharp(join(root,f.slug+'-book.svg'),{density:156}).resize(2040).png().withMetadata({density:300}).toFile(join(root,'book',f.slug+'.png'));
}
const nav=manifest.figures.map(f=>`<a href="#${f.slug}"><span>${String(f.number).padStart(2,'0')}</span>${esc(f.title)}</a>`).join('\n');
const figs=manifest.figures.map(f=>`<figure id="${f.slug}"><img src="${f.slug}.svg" width="1200" height="820" alt="${esc(f.caption)}" loading="lazy"><figcaption><p><strong>${esc(f.title)}</strong></p><p>${esc(f.caption)}</p><p class="files"><a href="${f.slug}.png" download>PNG</a><a href="${f.slug}.svg" download>Editable SVG</a><a href="#top">Back to list</a></p></figcaption></figure>`).join('\n');
await writeFile(join(root,'index.html'),`<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Support Machine · Illustrations</title><meta name="author" content="Assaf Barnir">
<style>*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:white;color:black;font-family:Arial,Helvetica,sans-serif;line-height:1.55}main{max-width:1264px;padding:48px 32px;margin:auto}.eyebrow{font-size:13px;letter-spacing:.1em;text-transform:uppercase;font-weight:bold}h1{font-size:clamp(32px,4vw,48px);line-height:1.1;margin:14px 0 22px}header>p{font-size:18px;max-width:800px}a{color:inherit;text-underline-offset:4px}nav{display:grid;grid-template-columns:1fr 1fr;gap:0 36px;margin:34px 0 60px}nav a{padding:14px 0;border-bottom:1px solid black;font-size:16px;text-decoration:none;display:flex;gap:14px}nav a:hover{text-decoration:underline}nav span{font-weight:bold;font-size:13px}figure{margin:0 0 72px;scroll-margin-top:24px}figure img{display:block;width:100%;height:auto}figcaption{max-width:940px;margin:12px 32px;font-size:17px}figcaption p{margin:8px 0}.files{display:flex;gap:24px;font-size:14px}footer{border-top:1px solid black;padding-top:20px;font-size:14px}a:focus-visible{outline:2px solid black;outline-offset:4px}@media(max-width:700px){main{padding:28px 12px}nav{grid-template-columns:1fr;margin-bottom:36px}figcaption{margin:12px}figure{margin-bottom:42px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}@media print{main{padding:0}header,nav,.files,footer{display:none}figure{break-inside:avoid;margin-bottom:24px}figcaption{font-size:12px}}
</style></head><body><main id="top"><header><p class="eyebrow">Assaf Barnir · The Support Machine · v0.3</p><h1>The machine, drawn out</h1><p>Six operating gates and four supporting ideas, drawn in black and white. Each figure also appears beside its discussion in the book.</p><p><a href="../book.html">Read the book</a> · <a href="../the-support-machine-v0.3.pdf">PDF</a></p></header><nav aria-label="Illustrations">${nav}</nav>${figs}<footer>Illustrations for The Support Machine by Assaf Barnir. <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.</footer></main></body></html>`);
console.log(`Rendered ${manifest.figures.length} full PNGs, book PNGs, and the illustration gallery.`);
