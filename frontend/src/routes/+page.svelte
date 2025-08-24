<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  import "animate.css";

  let songTitle: string = "Loading...";
  let songArtist: string = "Loading...";
  let songsAvailable: string[] = [];
  let audioPlayer: HTMLAudioElement;
  let isPlaying = false;
  let volume = 100;
  let lastVolume = 100;
  let interval: NodeJS.Timeout;
  let loading = true;

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

  async function fetchSongsAvailable() {
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
  }

  onMount(async () => {
    await Promise.all([fetchNowPlaying(), fetchSongsAvailable()]);
    loading = false;
    
    interval = setInterval(fetchNowPlaying, 10000);
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


  function skipSong() {
    fetch("http://127.0.0.1:5000/skip", { method: "GET" })
      .then((response) => {
        if (response.ok) {
          console.log("Song skipped");
        } else {
          console.error("Failed to skip song");
        }
      })
      .catch((error) => {
        console.error("Error skipping song:", error);
      });
  }


  function reloadWebsite() {
    location.reload();
  }
</script>

<audio
  bind:this={audioPlayer}
  src="http://127.0.0.1:8000/radio.ogg"
  preload="auto"
></audio>

<div class="bg-gray-900 py-16 sm:py-24">
  <div class="mx-auto max-w-2xl px-6 lg:max-w-7xl lg:px-8">
    <div class="flex">
      <div class="flex-1 w-48 mx-12 p-4 bg-gray-800 rounded-lg h-140">
        <img src="/img/synthwave.png" alt="Synthwave" class="rounded-lg" />
        {#if loading}
          <div class="animate-pulse mt-2">
            <div class="h-4 bg-gray-700 rounded w-3/4"></div>
            <div class="h-4 bg-gray-700 rounded w-1/2 mt-2"></div>
          </div>
        {:else}
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
        {/if}
        <div class="grid grid-cols-3">
          <div class="relative">
            <button
            onclick={reloadWebsite}
            class="absolute inset-y-0 right-9 w-[32px] fill-current text-[#3E6990] dark:text-white bg-transparent cursor-pointer"
            aria-label="Reload"
            >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M488 192l-144 0c-9.7 0-18.5-5.8-22.2-14.8s-1.7-19.3 5.2-26.2l46.7-46.7c-75.3-58.6-184.3-53.3-253.5 15.9-75 75-75 196.5 0 271.5s196.5 75 271.5 0c8.2-8.2 15.5-16.9 21.9-26.1 10.1-14.5 30.1-18 44.6-7.9s18 30.1 7.9 44.6c-8.5 12.2-18.2 23.8-29.1 34.7-100 100-262.1 100-362 0S-25 175 75 75c94.3-94.3 243.7-99.6 344.3-16.2L471 7c6.9-6.9 17.2-8.9 26.2-5.2S512 14.3 512 24l0 144c0 13.3-10.7 24-24 24z"/></svg>
        </button>
          
          </div>
          <div class="rounded-full">
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
          <div class="relative">
            <!-- button to skip -->
            <button
              onclick={(event) => {
              skipSong();
              const btn = event.currentTarget as HTMLButtonElement;
              btn.classList.add('animate__tada');
              setTimeout(() => btn.classList.remove('animate__tada'), 1000);
              }}
              class="w-12 fill-[#3E6990] dark:fill-white flex-1 absolute inset-y-0 right-4 cursor-pointer animate__animated"
              aria-label="Skip song"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512" class="w-[32px]">
              <path d="M371.7 43.1C360.1 32 343 28.9 328.3 35.2S304 56 304 72l0 136.3-172.3-165.1C120.1 32 103 28.9 88.3 35.2S64 56 64 72l0 368c0 16 9.6 30.5 24.3 36.8s31.8 3.2 43.4-7.9L304 303.7 304 440c0 16 9.6 30.5 24.3 36.8s31.8 3.2 43.4-7.9l192-184c7.9-7.5 12.3-18 12.3-28.9s-4.5-21.3-12.3-28.9l-192-184z"/>
              </svg>
            </button>
          </div>
        </div>


          
        
        <div class="flex mt-5">
          <button onclick={toggleMute} class="w-full fill-[#3E6990] dark:fill-white flex-1 cursor-pointer">
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
            {#if loading}
              {#each Array(30) as _}
                <tr>
                  <td class="py-2 border-b border-gray-700">
                    <div class="animate-pulse">
                      <div class="h-4 bg-gray-700 rounded w-5/6"></div>
                    </div>
                  </td>
                </tr>
              {/each}
            {:else}
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
            {/if}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
