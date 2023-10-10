import { build } from 'esbuild'
await build({
    entryPoints: ['mkdocs_pyscript/js/makeblocks.js', 'mkdocs_pyscript/js/mini-coi.js'],
    bundle: true,
    format: 'esm',
    outdir: 'mkdocs_pyscript/dist/js',
    external: ['@pyscript*']
})