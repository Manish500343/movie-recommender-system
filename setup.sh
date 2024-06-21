mkdir -p ~/.streamlit/

echo "\
[server]\n\
port=$PORT\n\
enableCORS= FALSE\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml