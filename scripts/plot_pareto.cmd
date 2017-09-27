setlocal

if [%ell_root%] == [] goto error

echo off
set "models_root=%cd%"

pushd %ell_root%\build\tools\utilities\pythonlibs\gallery
python plot_model_stats.py %models_root% -o speed_v_accuracy.png
move speed_v_accuracy.png %models_root%
move frontier_models.json %models_root%
popd
goto done

:error
echo "ell_root not set, please set it to the root of your ELL repository"

:done