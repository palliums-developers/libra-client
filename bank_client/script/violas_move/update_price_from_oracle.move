script {
use 0x7257c2417e4d1038e1817c8f283ace2e::ViolasBank;

fun main<Token>(account: &signer) {
    ViolasBank::update_price_from_oracle<Token>(account);
}
}
