setlocal

set "model_path=%cd%"
set ell_root=c:\work\ELL

pushd %ell_root%\build\tools\utilities\pythonlibs\gallery
python generate_md.py %model_path% %model_path%\model.md
popd

endlocal