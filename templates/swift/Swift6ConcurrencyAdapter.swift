//
//  Swift6ConcurrencyAdapter.swift
//  iOS 26 Adaptation Template
//
//  Helper patterns for migrating to Swift 6 strict concurrency checking.
//  Xcode 26 ships with Swift 6 and enables complete strict concurrency by default.
//

import Foundation

// MARK: - ViewModel with Main Actor

/// Mark UI-related view models with @MainActor to ensure all UI updates happen on the main thread.
@MainActor
final class MainActorViewModel: ObservableObject {
    @Published var items: [String] = []
    @Published var isLoading = false

    func loadData() async {
        isLoading = true
        defer { isLoading = false }

        // Offload heavy work to a background task
        let result = await Task.detached {
            // Background work here (e.g., network request, parsing)
            return ["Item 1", "Item 2", "Item 3"]
        }.value

        // Back on MainActor because this class is annotated
        self.items = result
    }
}

// MARK: - Sendable Data Model

/// Value types are automatically Sendable. Use structs for data models when possible.
struct UserProfile: Sendable {
    let id: String
    let name: String
    let email: String
}

// MARK: - @unchecked Sendable for Reference Types

/// Use @unchecked Sendable ONLY when you have manually verified thread safety.
/// Prefer actor isolation or value types instead.
final class SharedCache: @unchecked Sendable {
    private var storage: [String: Data] = [:]
    private let lock = NSLock()

    func set(_ data: Data, forKey key: String) {
        lock.lock()
        defer { lock.unlock() }
        storage[key] = data
    }

    func get(forKey key: String) -> Data? {
        lock.lock()
        defer { lock.unlock() }
        return storage[key]
    }
}

// MARK: - Async/Await replacing Completion Handlers

/// Before (Swift 5, completion handler):
/// ```
/// func fetchUser(userID: String, completion: @escaping (Result<UserProfile, Error>) -> Void) {
///     URLSession.shared.dataTask(with: url) { data, _, error in
///         // ... parse and call completion
///     }.resume()
/// }
/// ```

/// After (Swift 6, async/await):
func fetchUser(userID: String) async throws -> UserProfile {
    let url = URL(string: "https://api.example.com/users/\(userID)")!
    let (data, _) = try await URLSession.shared.data(from: url)
    let decoder = JSONDecoder()
    return try decoder.decode(UserProfile.self, from: data)
}

// MARK: - Bridging Non-Sendable to Sendable

/// When you must cross isolation boundaries with non-Sendable types,
/// transfer them explicitly using `nonisolated` + `@Sendable` closures.

nonisolated func processInBackground(data: Data) async -> String {
    return await Task.detached { @Sendable in
        // Process data in background (data is captured by value)
        return String(data: data, encoding: .utf8) ?? ""
    }.value
}

// MARK: - Replacing DispatchQueue.main.async

/// Before:
/// ```
/// DispatchQueue.global().async {
///     let result = heavyCalculation()
///     DispatchQueue.main.async {
///         self.label.text = result
///     }
/// }
/// ```

/// After (using @MainActor method):
extension MainActorViewModel {
    func updateUI(with result: String) {
        // This method is implicitly on MainActor because the class is annotated
        // label.text = result
    }

    func performHeavyWork() async {
        let result = await Task.detached {
            // Heavy calculation on background thread
            return "Computed Result"
        }.value

        // Safe to update UI here — we're on MainActor
        updateUI(with: result)
    }
}

// MARK: - Global Actor for Shared State

/// Use a custom global actor for shared mutable state that needs isolation
/// but doesn't belong to a specific view model.

@globalActor
actor DatabaseActor {
    static let shared = DatabaseActor()
}

@DatabaseActor
final class DatabaseManager {
    private var records: [String: Any] = [:]

    func saveRecord(id: String, value: Any) {
        records[id] = value
    }

    func getRecord(id: String) -> Any? {
        return records[id]
    }
}

/// Access from MainActor requires await
// @MainActor
// func loadFromDatabase() async {
//     let value = await DatabaseManager.shared.getRecord(id: "user_123")
// }
