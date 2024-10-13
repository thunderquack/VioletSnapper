Get-ChildItem camera_0*.jpg | Sort-Object Name | ForEach-Object { "file '$($_.Name)'" } > file_list.txt

ffmpeg -f concat -safe 0 -i file_list.txt -c:v libx264 -pix_fmt yuv420p -r 25 output.mp4