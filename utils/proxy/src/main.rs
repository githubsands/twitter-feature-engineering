#![deny(warnings)]
#![cfg_attr(debug_assertions, allow(dead_code, unused_imports))]

use bytes::Bytes;
use std::convert::From;
use std::net::SocketAddr;

use std::net::Incoming;
// use hyper::client::http1::Builder;
// use hyper::server::conn::http1;
use hyper::service::service_fn;
use hyper::upgrade::Upgraded;
use hyper::{Request, Response};

use tokio::io::Error;
use tokio::net::{TcpListener, TcpStream};

// route_twitter routes messages from the incoming client to the twitter servers
//
enum RouteError {
    NoMatchOccuredOnUpgrade(String),
    EstablishTCPStreamError(String),
}

impl From<Error> for RouteError {
    fn from(error: Error) -> Self {
        RouteError::NoMatchOccuredOnUpgrade(format!("{}", error))
    }
}

/*
async fn route_twitter(
    req: Request<Incoming<'_>>,
    addr: String,
) -> Result<Response<BoxBody<Bytes, hyper::Error>>, RouteError> {
    /*
    let join_handler = tokio::task::spawn_blocking(async move {
        match hyper::upgrade::on(req).await {
            // if upgrade occurs establish the tcp_stream and return a Response<BoxBody>
            Ok(upgraded) => {
                if let Err(e) = establish_tcp_stream(upgraded, addr).await {
                    eprintln!("server io error: {}", e);
                };
            }
            Err(e) => eprintln!("upgrade error: {}", e),
        });
    */
    // join_handler.await.unwrap();
}
*/

/*
fn empty() -> BoxBody<Bytes, hyper::Error> {
    Empty::<Bytes>::new()
        .map_err(|never| match never {})
        .boxed()
}
*/

fn main() {}

/*
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("starting twitter forwarder");
    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    let listener = TcpListener::bind(addr).await?;
    loop {
        let (_, _) = listener.accept().await?;
        tokio::task::spawn(async move {
            /*
            if let Err(err) = http1::Builder::new()
                .serve_connection(stream, service_fn(route_twitter))
                .await
            {
                println!("Error serving connection: {:?}", err);
            }
            */
        });
    }
}
*/

// establish_tcp_stream establishes a tcp stream between the machine
// that runs this server and the twitter servers
async fn establish_tcp_stream(
    mut upgraded: Upgraded,
    addr: String,
) -> Result<(u64, u64), RouteError> {
    let mut server = TcpStream::connect(addr).await?;
    let handler = tokio::io::copy_bidirectional(&mut upgraded, &mut server);
    let result = handler.await;
    match result {
        Ok(_) => return Ok(result.unwrap()),
        Err(_) => return Err(RouteError::EstablishTCPStreamError("test".to_string())),
    }
}
