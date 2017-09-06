setlocal

if [%ell_root%] == [] goto error

set "model_path=%cd%"

pushd %ell_root%\build\tools\utilities\pythonlibs\gallery
python generate_md.py %model_path% %model_path%\model.md
popd
goto done

:error
echo "ell_root not set, please set it to the root of your ELL repository"

:done
endlocal