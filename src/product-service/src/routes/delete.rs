use crate::model::ProductInfo;
use crate::startup::AppState;
use actix_web::{web, Error, HttpResponse};

pub async fn delete_product(
    data: web::Data<AppState>,
    path: web::Path<ProductInfo>,
) -> Result<HttpResponse, Error> {
    let mut products = match data.products.lock() {
        Ok(guard) => guard,
        Err(e) => {
            log::error!("Mutex poisoned in delete_product: {:?}", e);
            return Ok(HttpResponse::InternalServerError().body("Internal server error"));
        }
    };

    // find product by id in products
    let index = match products.iter().position(|p| p.id == path.product_id) {
        Some(idx) => idx,
        None => return Ok(HttpResponse::NotFound().body("Product not found"))
    };

    // remove product from products
    products.remove(index);

    Ok(HttpResponse::Ok().body(""))
}