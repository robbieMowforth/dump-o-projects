<?php
//made using the following tutorial
//https://levelup.gitconnected.com/4-steps-to-create-a-discord-bot-using-asynchronous-php-951082d7677a
/*
//$browser = new Browser($loop);
//use ($browser);
$browser->get('https://api.chucknorris.io/jokes/random')->then(function (ResponseInterface $response) use ($message) {
    $joke = json_decode($response->getBody())->value;
  });
*/

//To install composer please visit
//https://getcomposer.org/doc/00-intro.md

//Discord Bot in PHP docs: https://discord-php.github.io/DiscordPHP/#basics

//cd xampp\htdocs\projectSP\discordBot
//php bot.php
use Discord\Discord;
use Discord\Parts\Channel\Message;
use Psr\Http\Message\ResponseInterface;
use React\EventLoop\Factory;
use React\Http\Browser;

require __DIR__ . '/vendor/autoload.php';

//Includes from our files
//require_once 'includes\dbh.inc.php';
require 'C:\xampp\htdocs\projectSP\includes\dbFuncs.php';

$loop = Factory::create();

$discord = new Discord([
    'token' => '',
    'loop' => $loop,
]);

/*TODO:
- Find a way to make it so the bot recognizes the message isn't from a bot (stops infinite loop)
- Look into a beter method to get the $conn varibales, have to include the $conn variable each call.
- Add Error Handling, Expected input: !stats <PlayerID>
*/
$discord->on('message', function (Message $message, Discord $discord) {
    if ( substr(strtolower($message->content),0,6) == '!stats' && false !== substr(strtolower($message->content),6)  ) {

        require 'C:\xampp\htdocs\projectSP\includes\dbh.inc.php';
        $playerID = trim(substr($message->content,7));

        $result = getCollection($conn,$playerID);

        $message->reply($result);
    }
});

$discord->run();
