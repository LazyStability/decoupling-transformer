let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd ~/Software/decoupling-transformer
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +527 src/search/decoupling/mwis_factoring.cc
argglobal
%argdel
$argadd src/search/decoupling/mwis_factoring.cc
edit src/search/decoupling/mwis_factoring.cc
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
setlocal foldmethod=expr
setlocal foldexpr=v:lua.vim.treesitter.foldexpr()
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=99
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
23
sil! normal! zo
24
sil! normal! zo
24
sil! normal! zc
43
sil! normal! zo
43
sil! normal! zc
97
sil! normal! zc
152
sil! normal! zo
152
sil! normal! zc
169
sil! normal! zo
169
sil! normal! zc
199
sil! normal! zo
199
sil! normal! zc
221
sil! normal! zc
437
sil! normal! zo
467
sil! normal! zo
501
sil! normal! zo
544
sil! normal! zo
555
sil! normal! zc
561
sil! normal! zo
561
sil! normal! zc
586
sil! normal! zo
586
sil! normal! zc
626
sil! normal! zo
626
sil! normal! zc
708
sil! normal! zo
708
sil! normal! zc
820
sil! normal! zo
820
sil! normal! zc
850
sil! normal! zo
850
sil! normal! zc
861
sil! normal! zo
861
sil! normal! zc
916
sil! normal! zo
916
sil! normal! zc
1000
sil! normal! zo
1000
sil! normal! zc
1010
sil! normal! zo
1010
sil! normal! zc
1097
sil! normal! zc
1129
sil! normal! zo
1129
sil! normal! zc
1141
sil! normal! zo
1141
sil! normal! zc
let s:l = 532 - ((10 * winheight(0) + 26) / 52)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 532
normal! 09|
lcd ~/Software/decoupling-transformer
tabnext 1
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0 && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20
let &shortmess = s:shortmess_save
let &winminheight = s:save_winminheight
let &winminwidth = s:save_winminwidth
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &g:so = s:so_save | let &g:siso = s:siso_save
set hlsearch
nohlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
