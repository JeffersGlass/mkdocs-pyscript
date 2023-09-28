import { basicSetup, EditorView } from 'https://cdn.jsdelivr.net/npm/codemirror@6.0.1/+esm'
import { Compartment } from 'https://cdn.jsdelivr.net/npm/@codemirror/state@6.2.0/+esm'
import { python } from 'https://cdn.jsdelivr.net/npm/@codemirror/lang-python@6.1.3/+esm';
import { indentUnit } from 'https://cdn.jsdelivr.net/npm/@codemirror/language@6.6.0/+esm';
import { keymap } from 'https://cdn.jsdelivr.net/npm/@codemirror/view@6.9.3/+esm';
import { defaultKeymap } from 'https://cdn.jsdelivr.net/npm/@codemirror/commands@6.2.2/+esm';

const RUNBUTTON = `<svg style="height:20px;width:20px;vertical-align:-.125em;transform-origin:center;overflow:visible;color:green" viewBox="0 0 384 512" aria-hidden="true" role="img" xmlns="http://www.w3.org/2000/svg"><g transform="translate(192 256)" transform-origin="96 0"><g transform="translate(0,0) scale(1,1)"><path d="M361 215C375.3 223.8 384 239.3 384 256C384 272.7 375.3 288.2 361 296.1L73.03 472.1C58.21 482 39.66 482.4 24.52 473.9C9.377 465.4 0 449.4 0 432V80C0 62.64 9.377 46.63 24.52 38.13C39.66 29.64 58.21 29.99 73.03 39.04L361 215z" fill="currentColor" transform="translate(-192 -256)"></path></g></g></svg>`;

function makeEditor(pySrc, parent) {
    const languageConf = new Compartment();
    const extensions = [
        indentUnit.of('    '),
        basicSetup,
        languageConf.of(python()),
        keymap.of([
            ...defaultKeymap,
            { key: 'Ctrl-Enter', run: , preventDefault: true },
            { key: 'Shift-Enter', run: , preventDefault: true },
        ]),
    ];

    /*if (this.getAttribute('theme') === 'dark') {
        extensions.push(oneDarkTheme);
    } */

    return new EditorView({
        doc: pySrc,
        extensions,
        parent,
    });
}

window.makePyEditor = makeEditor
