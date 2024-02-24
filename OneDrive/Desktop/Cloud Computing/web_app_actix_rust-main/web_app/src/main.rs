use actix_web::{web, App, HttpServer, Responder};
use rand::Rng;

fn is_prime(num: u64) -> bool {
    if num <= 1 {
        return false;
    }
    for i in 2..=(num as f64).sqrt() as u64 {
        if num % i == 0 {
            return false;
        }
    }
    true
}

async fn generate_random_prime() -> impl Responder {
    let mut rng = rand::thread_rng();
    let mut num = rng.gen_range(1000..10000);

    while !is_prime(num) {
        num = rng.gen_range(1000..10000);
    }

    format!("Random Prime Number: {}", num)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .route("/", web::get().to(generate_random_prime))
    })
    .bind("0.0.0.0:8080")?
    .run()
    .await
}
