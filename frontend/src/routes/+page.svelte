<script lang="ts">
  import { onDestroy, onMount } from "svelte";

  let songTitle: string = "Loading...";
  let songArtist: string = "Loading...";
  let songsAvailable: string[] = [];
  let audioPlayer: HTMLAudioElement;
  let isPlaying = false;
  let volume = 100;
  let lastVolume = 100;
  let interval: NodeJS.Timeout;

  $: if (audioPlayer) audioPlayer.volume = volume / 100;


  async function fetchNowPlaying() {
    try {
    const response = await fetch("http://127.0.0.1:5000/now-playing");
    if (response.ok) {
      const data = await response.json();
      songTitle = data.title || "Title not available";
      songArtist = data.artist || "Artist not available";
    } else {
      songTitle = "Error fetching song info.";
      songArtist = "Error fetching artist info.";
    }
    } catch (error) {
    console.error("Failed to fetch now playing data:", error);
    songTitle = "Could not connect to the server.";
    }
  }

  onMount(async () => {
    await fetchNowPlaying();
    interval = setInterval(fetchNowPlaying, 10000);

    try {
      const response = await fetch("http://127.0.0.1:5000/songsAvailable");
      if (response.ok) {
        const data = await response.json();
        songsAvailable = data.musicfiles || [];
      } else {
        songsAvailable = [];
      }
    } catch (error) {
      console.error("Failed to fetch songs data:", error);
      songsAvailable = [];
    }
  });

  onDestroy(() => {
    clearInterval(interval);
  });

  function togglePlay() {
    if (isPlaying) {
      audioPlayer.pause();
    } else {
      audioPlayer.play();
    }
    isPlaying = !isPlaying;
  }

  function toggleMute() {
    if (volume > 0) {
      lastVolume = volume;
      volume = 0;
    } else {
      volume = lastVolume;
    }
  }
</script>

<audio
  bind:this={audioPlayer}
  src="http://127.0.0.1:8000/radio.ogg"
  preload="none"
></audio>

<div class="bg-gray-900 py-16 sm:py-24">
  <div class="mx-auto max-w-2xl px-6 lg:max-w-7xl lg:px-8">
    <div class="flex">
      <div class="flex-1 w-48 mx-12 p-4 bg-gray-800 rounded-lg h-140">
        <img src="/img/synthwave.png" alt="Synthwave" class="rounded-lg" />
        <div class="rounded-full">
          <div class="justify-center">
            <p
              class="text-white dark:text-[#FAF9EF] text-lg mt-2"
              id="songname"
            >
              {songTitle}
            </p>
            <p
              class="text-white dark:text-[#FAF9EF] text-md"
              id="artistname"
            >
              {songArtist}
            </p>
            <button
              onclick={togglePlay}
              class="cursor-pointer mx-auto mt-2 w-24 h-24 rounded-full bg-white border shadow-xl flex items-center justify-center dark:bg-[#3E6990]"
            >
              {#if isPlaying}
                <!-- Pause Icon -->
                <svg
                  width="48"
                  height="48"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  class="fill-[#3E6990] dark:fill-white"
                >
                  <path d="M10 4H6V20H10V4Z" />
                  <path d="M18 4H14V20H18V4Z" />
                </svg>
              {:else}
                <!-- Play Icon -->
                <svg
                  id="play-icon"
                  class="ml-[10px]"
                  width="31"
                  height="37"
                  viewBox="0 0 31 37"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    fill-rule="evenodd"
                    clip-rule="evenodd"
                    d="M29.6901 16.6608L4.00209 0.747111C2.12875 -0.476923 0.599998 0.421814 0.599998 2.75545V33.643C0.599998 35.9728 2.12747 36.8805 4.00209 35.6514L29.6901 19.7402C29.6901 19.7402 30.6043 19.0973 30.6043 18.2012C30.6043 17.3024 29.6901 16.6608 29.6901 16.6608Z"
                    class="fill-[#3E6990] dark:fill-white"
                  ></path>
                </svg>
              {/if}
            </button>
          </div>
        </div>
        <div class="flex mt-5">
          <button onclick={toggleMute} class="w-full fill-[#3E6990] dark:fill-white flex-1">
            {#if volume > 75}
              <!-- High Volume Icon -->
              <div class="w-10">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="20 0 640 512"><path d="M533.6 32.5c-10.3-8.4-25.4-6.8-33.8 3.5s-6.8 25.4 3.5 33.8C557.5 113.8 592 180.8 592 256s-34.5 142.2-88.7 186.3c-10.3 8.4-11.8 23.5-3.5 33.8s23.5 11.8 33.8 3.5C598.5 426.7 640 346.2 640 256S598.5 85.2 533.6 32.5zM473.1 107c-10.3-8.4-25.4-6.8-33.8 3.5s-6.8 25.4 3.5 33.8C475.3 170.7 496 210.9 496 256s-20.7 85.3-53.2 111.8c-10.3 8.4-11.8 23.5-3.5 33.8s23.5 11.8 33.8 3.5c43.2-35.2 70.9-88.9 70.9-149s-27.7-113.8-70.9-149zm-60.5 74.5c-10.3-8.4-25.4-6.8-33.8 3.5s-6.8 25.4 3.5 33.8C393.1 227.6 400 241 400 256s-6.9 28.4-17.7 37.3c-10.3 8.4-11.8 23.5-3.5 33.8s23.5 11.8 33.8 3.5C434.1 312.9 448 286.1 448 256s-13.9-56.9-35.4-74.5zM80 352l48 0 134.1 119.2c6.4 5.7 14.6 8.8 23.1 8.8 19.2 0 34.8-15.6 34.8-34.8l0-378.4c0-19.2-15.6-34.8-34.8-34.8-8.5 0-16.7 3.1-23.1 8.8L128 160 80 160c-26.5 0-48 21.5-48 48l0 96c0 26.5 21.5 48 48 48z"/></svg>
              </div>
            {:else if volume > 50}
              <!-- High Volume Icon -->
              <div class="w-10">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="20 0 640 512"><path d="M473.1 107c-10.3-8.4-25.4-6.8-33.8 3.5s-6.8 25.4 3.5 33.8C475.3 170.7 496 210.9 496 256s-20.7 85.3-53.2 111.8c-10.3 8.4-11.8 23.5-3.5 33.8s23.5 11.8 33.8 3.5c43.2-35.2 70.9-88.9 70.9-149s-27.7-113.8-70.9-149zm-60.5 74.5c-10.3-8.4-25.4-6.8-33.8 3.5s-6.8 25.4 3.5 33.8C393.1 227.6 400 241 400 256s-6.9 28.4-17.7 37.3c-10.3 8.4-11.8 23.5-3.5 33.8s23.5 11.8 33.8 3.5C434.1 312.9 448 286.1 448 256s-13.9-56.9-35.4-74.5zM80 352l48 0 134.1 119.2c6.4 5.7 14.6 8.8 23.1 8.8 19.2 0 34.8-15.6 34.8-34.8l0-378.4c0-19.2-15.6-34.8-34.8-34.8-8.5 0-16.7 3.1-23.1 8.8L128 160 80 160c-26.5 0-48 21.5-48 48l0 96c0 26.5 21.5 48 48 48z"/></svg>  
              </div>
            {:else if volume > 0}
              <!-- Volume Icon -->
              <div class="w-7">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M48 352l48 0 134.1 119.2c6.4 5.7 14.6 8.8 23.1 8.8 19.2 0 34.8-15.6 34.8-34.8l0-378.4c0-19.2-15.6-34.8-34.8-34.8-8.5 0-16.7 3.1-23.1 8.8L96 160 48 160c-26.5 0-48 21.5-48 48l0 96c0 26.5 21.5 48 48 48zM380.6 181.5c-10.3-8.4-25.4-6.8-33.8 3.5s-6.8 25.4 3.5 33.8C361.1 227.6 368 241 368 256s-6.9 28.4-17.7 37.3c-10.3 8.4-11.8 23.5-3.5 33.8s23.5 11.8 33.8 3.5C402.1 312.9 416 286.1 416 256s-13.9-56.9-35.5-74.5z"/></svg>
              </div>
            {:else}
              <!-- Muted Icon -->
              <div class="w-9">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M48 352l48 0 134.1 119.2c6.4 5.7 14.6 8.8 23.1 8.8 19.2 0 34.8-15.6 34.8-34.8l0-378.4c0-19.2-15.6-34.8-34.8-34.8-8.5 0-16.7 3.1-23.1 8.8L96 160 48 160c-26.5 0-48 21.5-48 48l0 96c0 26.5 21.5 48 48 48zM367 175c-9.4 9.4-9.4 24.6 0 33.9l47 47-47 47c-9.4 9.4-9.4 24.6 0 33.9s24.6 9.4 33.9 0l47-47 47 47c9.4 9.4 24.6 9.4 33.9 0s9.4-24.6 0-33.9l-47-47 47-47c9.4-9.4 9.4-24.6 0-33.9s-24.6-9.4-33.9 0l-47 47-47-47c-9.4-9.4-24.6-9.4-33.9 0z"/></svg>
              </div>
            {/if}
          </button>

          <input
            type="range"
            class="w-120 flex-4"
            min="0"
            max="100"
            step="1"
            bind:value={volume}
          />
        </div>
      </div>

      <div class="flex-2 w-96 px-12">
        <h2
          class="text-white dark:text-[#FAF9EF] text-3xl font-extrabold tracking-tight sm:text-4xl"
        >
          Songs Available
        </h2>
        <table class="mt-4 w-full text-left border-collapse">
          <thead>
            <tr>
              <th class="text-white dark:text-[#FAF9EF] text-lg border-b pb-2">
                {" "}
              </th>
            </tr>
          </thead>
          <tbody>
            {#each songsAvailable as song}
              {#if song.match(/^[^"'＂]+["'＂](.*?)["'＂]\s+by\s+([^[]+)/i)}
              {@const match = song.match(/^[^"＂']+["＂'](.*?)["＂']\s+by\s+([^[]+)/i)}
              <tr>
                <td class="text-white dark:text-[#FAF9EF] py-2 border-b">
                  <a
                    href="#"
                    onclick={async () => {
                      await fetch(
                        `http://127.0.0.1:5000/request?uri=${encodeURIComponent(
                          song
                        )}`
                      );
                    }}
                  >
                    <span class="font-bold">{match[1]}</span>{" "}
                    <span class="italic">by {match[2]}</span>
                  </a>
                </td>
              </tr>
              {:else}
              <tr>
                <td class="text-white dark:text-[#FAF9EF] py-2 border-b">
                  {song}
                </td>
              </tr>
              {/if}
            {/each}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
