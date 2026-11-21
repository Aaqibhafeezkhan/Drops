use std::process::Command;

fn main() {
    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rerun-if-changed=.git/HEAD");
    println!("cargo:rerun-if-env-changed=GITHUB_SHA");
    let version = std::env::var("CARGO_PKG_VERSION").expect("Cargo package version");
    let commit = std::env::var("GITHUB_SHA")
        .ok()
        .filter(|value| value.len() >= 12 && value.chars().all(|c| c.is_ascii_hexdigit()))
        .map(|value| value[..12].to_owned())
        .or_else(|| Command::new("git")
            .args(["rev-parse", "--short=12", "HEAD"])
            .output()
            .ok()
            .filter(|output| output.status.success())
            .and_then(|output| String::from_utf8(output.stdout).ok())
            .map(|value| value.trim().to_owned())
            .filter(|value| !value.is_empty()));
    let long_version = match commit {
        Some(commit) => format!("{version} ({commit})"),
        None => version,
    };
    println!("cargo:rustc-env=DROPS_LONG_VERSION={long_version}");
}
