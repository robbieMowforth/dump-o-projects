<?php

/*
 * This file is apart of the DiscordPHP project.
 *
 * Copyright (c) 2021 David Cole <david.cole1340@gmail.com>
 *
 * This source file is subject to the MIT license that is bundled
 * with this source code in the LICENSE.md file.
 */

namespace Discord\Parts\Permissions;

/**
 * {@inheritdoc}
 *
 * @property bool $priority_speaker
 * @property bool $stream
 * @property bool $connect
 * @property bool $speak
 * @property bool $mute_members
 * @property bool $deafen_members
 * @property bool $move_members
 * @property bool $use_vad
 *
 * @property bool $add_reactions
 * @property bool $send_messages
 * @property bool $send_tts_messages
 * @property bool $manage_messages
 * @property bool $embed_links
 * @property bool $attach_files
 * @property bool $read_message_history
 * @property bool $mention_everyone
 * @property bool $use_external_emojis
 */
class ChannelPermission extends Permission
{
    /**
     * {@inheritdoc}
     */
    public static function getPermissions(): array
    {
        return array_merge(parent::ALL_PERMISSIONS, parent::TEXT_PERMISSIONS, parent::VOICE_PERMISSIONS);
    }
}
