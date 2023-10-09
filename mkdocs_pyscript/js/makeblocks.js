import { basicSetup, EditorView } from 'https://cdn.jsdelivr.net/npm/codemirror@6.0.1/+esm'
import { EditorState, Compartment } from 'https://cdn.jsdelivr.net/npm/@codemirror/state@6.2.1/+esm'
import { python } from 'https://cdn.jsdelivr.net/npm/@codemirror/lang-python/+esm';
import { indentUnit } from 'https://cdn.jsdelivr.net/npm/@codemirror/language/+esm';
import { keymap } from 'https://cdn.jsdelivr.net/npm/@codemirror/view@6.9.3/+esm';
import { defaultKeymap } from 'https://cdn.jsdelivr.net/npm/@codemirror/commands@6.2.2/+esm';
import {$, $$} from 'https://cdn.jsdelivr.net/npm/basic-devtools@0.1.6/+esm'
import { PyWorker } from "https://cdn.jsdelivr.net/npm/@pyscript/core";

const RUNBUTTON = `<svg style="height:20px;width:20px;vertical-align:-.125em;transform-origin:center;overflow:visible;color:green" viewBox="0 0 384 512" aria-hidden="true" role="img" xmlns="http://www.w3.org/2000/svg"><g transform="translate(192 256)" transform-origin="96 0"><g transform="translate(0,0) scale(1,1)"><path d="M361 215C375.3 223.8 384 239.3 384 256C384 272.7 375.3 288.2 361 296.1L73.03 472.1C58.21 482 39.66 482.4 24.52 473.9C9.377 465.4 0 449.4 0 432V80C0 62.64 9.377 46.63 24.52 38.13C39.66 29.64 58.21 29.99 73.03 39.04L361 215z" fill="currentColor" transform="translate(-192 -256)"></path></g></g></svg>`;

function addButtons(){
    const wrappers = document.querySelectorAll(".py-wrapper")

    wrappers.forEach(wrapper => {
        const pySrc = wrapper.textContent

        console.warn("CREATING BUTTON", wrapper)
        const btn = document.createElement('a')
        btn.style.cssText = "position:absolute; width:80px; height:30px; bottom:3px; right:3px; background-color:#7773f7; color:#FFF; border-radius:5px; text-align:center; box-shadow: 2px 2px 3px #999; cursor:pointer"
        btn.addEventListener("click", replaceWithEditor.bind(btn, pySrc, wrapper))

        const label = document.createElement('i')
        label.style.cssText = "color:white;position:absolute; top:4px; left: 14px "
        label.innerText = "LOAD"

        btn.appendChild(label)
        wrapper.appendChild(btn)
    })
}

let _uniqueIdCounter = 0;
function ensureUniqueId(el) {
    if (el.id === '') el.id = `py-internal-${_uniqueIdCounter++}`;
}

class PyRepl extends HTMLElement {
    outDiv ;
    editor ;
    stdout_manager;
    stderr_manager;
    static observedAttributes = ['src'];
    connectedCallback() {
        ensureUniqueId(this);

        if (!this.hasAttribute('exec-id')) {
            this.setAttribute('exec-id', '0');
        }
        if (!this.hasAttribute('root')) {
            this.setAttribute('root', this.id);
        }

        const pySrc = ""
        this.innerHTML = '';
        const boxDiv = this.makeBoxDiv();
        const shadowRoot = $('.py-repl-editor > div', boxDiv).attachShadow({ mode: 'open' });
        // avoid inheriting styles from the outer component
        shadowRoot.innerHTML = `<style> :host { all: initial; }</style>`;
        this.appendChild(boxDiv);
        this.editor = this.makeEditor(pySrc, shadowRoot);
        this.editor.focus();
        console.debug(`element ${this.id} successfully connected`);
    }


    /** Create and configure the codemirror editor
     */
    makeEditor(pySrc, parent) {
        const languageConf = new Compartment();
        const extensions = [
            indentUnit.of('    '),
            languageConf.of(python()),
            keymap.of([
                ...defaultKeymap,
                { key: 'Ctrl-Enter', run: this.execute.bind(this), preventDefault: true },
                { key: 'Shift-Enter', run: this.execute.bind(this), preventDefault: true },
            ]),
            basicSetup,
        ];

        if (this.getAttribute('theme') === 'dark') {
            extensions.push(oneDarkTheme);
        }

        return new EditorView({
            doc: pySrc,
            extensions: extensions,
            parent: parent,
        });
    }

    // ******** main entry point for py-repl DOM building **********
    //
    // The following functions are written in a top-down, depth-first
    // order (so that the order of code roughly matches the order of
    // execution)
    makeBoxDiv() {
        const boxDiv = document.createElement('div');
        boxDiv.className = 'py-repl-box';

        const editorDiv = this.makeEditorDiv();
        this.outDiv = this.makeOutDiv();

        boxDiv.appendChild(editorDiv);
        boxDiv.appendChild(this.outDiv);

        return boxDiv;
    }

    makeEditorDiv() {
        const editorDiv = document.createElement('div');
        editorDiv.className = 'py-repl-editor';
        editorDiv.setAttribute('aria-label', 'Python Script Area');

        const runButton = this.makeRunButton();
        const editorShadowContainer = document.createElement('div');

        // avoid outer elements intercepting key events (reveal as example)
        editorShadowContainer.addEventListener('keydown', event => {
            event.stopPropagation();
        });

        editorDiv.append(editorShadowContainer, runButton);

        return editorDiv;
    }

    makeRunButton() {
        const runButton = document.createElement('button');
        runButton.className = 'absolute py-repl-run-button';
        runButton.innerHTML = RUNBUTTON;
        runButton.setAttribute('aria-label', 'Python Script Run Button');
        runButton.addEventListener('click', this.execute.bind(this));
        return runButton;
    }

    makeOutDiv() {
        const outDiv = document.createElement('div');
        outDiv.className = 'py-repl-output';
        outDiv.id = this.id + '-repl-output';
        return outDiv;
    }

    //  ********************* execution logic *********************

    /** Execute the python code written in the editor, and automatically
     *  display() the last evaluated expression
     */
    async execute() {
        const pySrc = `
import sys
from pyscript import sync

class MyStdout:
    def write(self, line):
        sync.write(line)

class MyStderr:
    def write(self, line):
        sync.writeErr(line)

sys.stdout = MyStdout()  
sys.stderr = MyStderr()   

${this.getPySrc()}
`;

        console.warn(`Running code ${pySrc}`)

        const srcLink = URL.createObjectURL((new Blob([pySrc])))
        console.log(srcLink)

        this.outDiv.innerHTML = ""
        const worker = PyWorker(srcLink, {hooks: {onWorkerReady: 'console.log.("worker is GO")'}});
        worker.sync.write = (str) => {this.outDiv.innerText += str}
        worker.sync.writeErr = (str) => {this.outDiv.innerHTML += `<span style='color:red'>${str}</span>`}
        worker.onerror = ({error}) => {this.outDiv.innerHTML += `<span style='color:red'>${str}</span>`; console.log(error)}
    }

    getPySrc() {
        return this.editor.state.doc.toString();
    }

    // XXX the autogenerate logic is very messy. We should redo it, and it
    // should be the default.
    autogenerateMaybe() {
        if (this.hasAttribute('auto-generate')) {
            const allPyRepls = $$(`py-repl[root='${this.getAttribute('root')}'][exec-id]`, document);
            const lastRepl = allPyRepls[allPyRepls.length - 1];
            const lastExecId = lastRepl.getAttribute('exec-id');
            const nextExecId = parseInt(lastExecId) + 1;

            const newPyRepl = document.createElement('py-repl');

            //Attributes to be copied from old REPL to auto-generated REPL
            for (const attribute of ['root', 'output-mode', 'output', 'stderr']) {
                const attr = this.getAttribute(attribute);
                if (attr) {
                    newPyRepl.setAttribute(attribute, attr);
                }
            }

            newPyRepl.id = this.getAttribute('root') + '-' + nextExecId.toString();

            if (this.hasAttribute('auto-generate')) {
                newPyRepl.setAttribute('auto-generate', '');
                this.removeAttribute('auto-generate');
            }

            newPyRepl.setAttribute('exec-id', nextExecId.toString());
            if (this.parentElement) {
                this.parentElement.appendChild(newPyRepl);
            }
        }
    }
}

customElements.define("py-repl", PyRepl)

function replaceWithEditor(pySrc, parent){
    const repl = document.createElement("py-repl")
    parent.innerHTML = ""
    parent.appendChild(repl)

    console.log({pySrc})

    //Insert PySrc
    repl.editor.dispatch({changes: {
        from: 0,
        to: repl.editor.state.doc.length,
        insert: pySrc
    }})
    
    console.log("Done setting source/")
}

addButtons();