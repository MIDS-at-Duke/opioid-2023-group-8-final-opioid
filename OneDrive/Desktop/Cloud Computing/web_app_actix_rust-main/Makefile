install:
	cargo clean &&\
		cargo build -j 1

build:
	docker build -t rust_web_app .

execdocker:
	docker run -dp 8080:8080 rust_web_app

format:
	cargo fmt --quiet

lint:
	cargo clippy --quiet

test:
	cargo test --quiet

run:
	cargo run 

all: format lint test run
