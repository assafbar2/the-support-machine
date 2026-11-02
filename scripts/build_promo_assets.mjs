/** Generate edition artwork from an approved book illustration. */
import {createRequire} from 'node:module';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const root=join(dirname(fileURLToPath(import.meta.url)),'..');
const modules=process.env.SUPPORT_NODE_MODULES;
const require=modules?createRequire(join(modules,'loader.js')):createRequire(import.meta.url);
const sharp=require('sharp');
const artwork=(await readFile(join(root,'docs/illustrations/book/02-choose-the-machine.png'))).toString('base64');
const target=join(root,'docs/assets');
await mkdir(target,{recursive:true});
const svg=(width,height,body)=>`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}"><rect width="100%" height="100%" fill="#fbfaf6"/>${body}</svg>`;
const social=svg(1200,630,`<path d="M62 80H1138M62 554H1138" stroke="#d8d2c5"/>
<text x="62" y="55" font-family="Arial,sans-serif" font-size="17" font-weight="700" letter-spacing="2" fill="#772817">SECOND EDITION</text>
<text x="62" y="210" font-family="Georgia,serif" font-size="81" fill="#141414">The Support</text>
<text x="62" y="297" font-family="Georgia,serif" font-size="81" fill="#141414">Machine</text>
<text x="65" y="362" font-family="Arial,sans-serif" font-size="24" fill="#514f48">How to Deploy AI in Customer Support</text>
<text x="65" y="397" font-family="Arial,sans-serif" font-size="24" fill="#514f48">Without Breaking Trust</text>
<text x="65" y="478" font-family="Arial,sans-serif" font-size="22" fill="#141414">Assaf Barnir</text>
<rect x="658" y="159" width="480" height="310" fill="white" stroke="#d8d2c5"/>
<image href="data:image/png;base64,${artwork}" x="677" y="193" width="442" height="215"/>
<text x="681" y="443" font-family="Georgia,serif" font-style="italic" font-size="17" fill="#514f48">Choose the layer before choosing the answer.</text>
<text x="62" y="593" font-family="Arial,sans-serif" font-size="18" fill="#514f48">29 chapters · 10 illustrations · 80 practical prompts · Free</text>`);
const cover=svg(800,1000,`<path d="M58 108H742M58 896H742" stroke="#d8d2c5"/>
<text x="58" y="73" font-family="Arial,sans-serif" font-size="20" font-weight="700" letter-spacing="3" fill="#772817">SECOND EDITION</text>
<text x="56" y="230" font-family="Georgia,serif" font-size="92" fill="#141414">The Support</text>
<text x="56" y="328" font-family="Georgia,serif" font-size="92" fill="#141414">Machine</text>
<text x="60" y="393" font-family="Arial,sans-serif" font-size="25" fill="#514f48">How to Deploy AI in Customer Support</text>
<text x="60" y="432" font-family="Arial,sans-serif" font-size="25" fill="#514f48">Without Breaking Trust</text>
<image href="data:image/png;base64,${artwork}" x="58" y="508" width="684" height="333"/>
<text x="58" y="946" font-family="Georgia,serif" font-size="30" fill="#141414">Assaf Barnir</text>
<text x="742" y="944" text-anchor="end" font-family="Arial,sans-serif" font-size="16" fill="#514f48">A practical field guide</text>`);
for (const [name,source] of [['second-edition-social',social],['second-edition-cover',cover]]) {
  await writeFile(join(target,name+'.svg'),source);
  await sharp(Buffer.from(source)).png().toFile(join(target,name+'.png'));
}
console.log('Generated Second Edition cover and social artwork.');
