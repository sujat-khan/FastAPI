"""
Module 01 - Lesson 03: Python Async Examples
=============================================
Run this file to see async vs sync behavior:
    python examples.py
"""

import asyncio
import time


# ============================================================
# Example 1: Sync vs Async Sleep
# ============================================================

def sync_task(name: str, seconds: int) -> str:
    """A synchronous function that blocks."""
    print(f"  [SYNC] {name} starting...")
    time.sleep(seconds)  # Blocks the entire thread
    print(f"  [SYNC] {name} finished after {seconds}s")
    return f"{name}_result"


async def async_task(name: str, seconds: int) -> str:
    """An async function that yields control while waiting."""
    print(f"  [ASYNC] {name} starting...")
    await asyncio.sleep(seconds)  # Yields control to event loop
    print(f"  [ASYNC] {name} finished after {seconds}s")
    return f"{name}_result"


# ============================================================
# Example 2: Sequential vs Concurrent Execution
# ============================================================

async def run_sequential():
    """Run tasks one after another (slow)."""
    print("\n--- Sequential Execution ---")
    start = time.time()

    result_a = await async_task("Task-A", 2)
    result_b = await async_task("Task-B", 2)
    result_c = await async_task("Task-C", 2)

    elapsed = time.time() - start
    print(f"  Results: {result_a}, {result_b}, {result_c}")
    print(f"  Total time: {elapsed:.1f}s (expected ~6s)\n")


async def run_concurrent():
    """Run tasks concurrently using asyncio.gather (fast!)."""
    print("\n--- Concurrent Execution ---")
    start = time.time()

    result_a, result_b, result_c = await asyncio.gather(
        async_task("Task-A", 2),
        async_task("Task-B", 2),
        async_task("Task-C", 2),
    )

    elapsed = time.time() - start
    print(f"  Results: {result_a}, {result_b}, {result_c}")
    print(f"  Total time: {elapsed:.1f}s (expected ~2s)\n")


# ============================================================
# Example 3: Real-World Pattern — Fetching Multiple Resources
# ============================================================

async def fetch_user(user_id: int) -> dict:
    """Simulate fetching a user from a database."""
    await asyncio.sleep(1)  # Simulate DB query
    return {"id": user_id, "name": f"User_{user_id}"}


async def fetch_user_posts(user_id: int) -> list:
    """Simulate fetching a user's posts."""
    await asyncio.sleep(1.5)  # Simulate DB query
    return [
        {"id": 1, "title": f"Post by User_{user_id}"},
        {"id": 2, "title": f"Another post by User_{user_id}"},
    ]


async def fetch_user_profile(user_id: int) -> dict:
    """Fetch user and their posts concurrently."""
    print(f"\n--- Fetching profile for user {user_id} ---")
    start = time.time()

    # Both queries run at the same time!
    user, posts = await asyncio.gather(
        fetch_user(user_id),
        fetch_user_posts(user_id),
    )

    elapsed = time.time() - start
    profile = {**user, "posts": posts}
    print(f"  Profile: {profile}")
    print(f"  Fetched in {elapsed:.1f}s (instead of 2.5s sequentially)")
    return profile


# ============================================================
# Example 4: asyncio.create_task for Background Work
# ============================================================

async def send_notification(message: str):
    """Simulate sending a notification (background task)."""
    print(f"  📨 Sending notification: '{message}'...")
    await asyncio.sleep(2)
    print(f"  ✅ Notification sent: '{message}'")


async def process_order(order_id: int):
    """Process an order and send notifications concurrently."""
    print(f"\n--- Processing Order #{order_id} ---")

    # Start notification in the background (don't wait for it)
    notification_task = asyncio.create_task(
        send_notification(f"Order #{order_id} received!")
    )

    # Process the order (this runs while notification is being sent)
    print(f"  Processing order #{order_id}...")
    await asyncio.sleep(1)
    print(f"  Order #{order_id} processed!")

    # Wait for notification to finish
    await notification_task
    print(f"  Everything done for order #{order_id}")


# ============================================================
# Main — Run All Examples
# ============================================================

async def main():
    print("=" * 50)
    print("  PYTHON ASYNC EXAMPLES")
    print("=" * 50)

    # Example 2: Sequential vs Concurrent
    await run_sequential()
    await run_concurrent()

    # Example 3: Real-world pattern
    await fetch_user_profile(42)

    # Example 4: Background tasks
    await process_order(101)

    print("\n" + "=" * 50)
    print("  ALL EXAMPLES COMPLETE!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
