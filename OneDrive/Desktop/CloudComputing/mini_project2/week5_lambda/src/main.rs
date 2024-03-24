use serde::{Deserialize, Serialize};
use serde_json::{Value, json};
use std::collections::HashMap;
use aws_sdk_dynamodb::{Client, model::AttributeValue};
use aws_config::{load_from_env};
use lambda_runtime::{service_fn, LambdaEvent, Error};
use tracing::{info, Level};
use tracing_subscriber::FmtSubscriber;
use chrono::Utc;


#[derive(Deserialize, Serialize)]
struct Event {
    name: String,
    age: u8,
}

#[derive(Serialize)]
struct LambdaResponse {
    statusCode: u16,
    headers: HashMap<String, String>,
    body: String,
}

#[tokio::main]
async fn main() -> Result<(), Error> {
    // Initialize logging
    let subscriber = FmtSubscriber::builder()
        .with_max_level(Level::INFO)
        .finish();
    
    tracing::subscriber::set_global_default(subscriber).expect("Unable to set global default");

    info!("Starting the ManagerWithLog service");

    let func = service_fn(handler);
    lambda_runtime::run(func).await?;
    Ok(())
}

async fn handler(_event: LambdaEvent<Value>) -> Result<Value, Error> {    
    let event: Event = serde_json::from_value(_event.payload)
        .map_err(|e| {
            tracing::error!("Error deserializing event to Request: {:?}", e); 
            Error::from(e.to_string())
        })?;

    let response = save_person(event).await?;

    Ok(response)
}

async fn save_person(event: Event) -> Result<Value, Error> {
    let config = load_from_env().await;
    let client = Client::new(&config);
    let table_name = "manager";

    let name = event.name.clone();
    let age = event.age.clone();
    let time = Utc::now();

    let mut item = HashMap::new();
    item.insert("name".to_string(), AttributeValue::S(name.clone()));
    item.insert("age".to_string(), AttributeValue::N(age.to_string()));
    item.insert("time".to_string(), AttributeValue::S(time.to_string()));

    client.put_item()
        .table_name(table_name)
        .set_item(Some(item))
        .send()
        .await
        .map_err(|e| {
            tracing::error!("Error saving person: {:?}", e);
            Error::from(e.to_string())
        });

    let message = format!("Inserted person record: {}, {} years old", name, age);
    // Create a JSON value directly for the response
    let response = json!({
        "statusCode": 200,
        "headers": { "Content-Type": "application/json" },
        "body": message,
    });

    Ok(response)
}
